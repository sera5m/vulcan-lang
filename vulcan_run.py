#!/usr/bin/env python3
"""Desktop Vulcan runner. LUT sin/cos wrap. No GTK required."""
from __future__ import annotations
import math, re, sys
SIN_Q15 = [int(round(math.sin(2 * math.pi * i / 256) * 32767)) for i in range(256)]

def _phase_from_deg(deg: int) -> int:
    return (int(deg) * 11930465) & 0xFFFFFFFF

def _lut_lerp(table, ph: int) -> int:
    i = (ph >> 24) & 255
    j = (i + 1) & 255
    f = (ph >> 16) & 255
    a, b = table[i], table[j]
    return a + (((b - a) * f) >> 8)

def lut_sin_deg(deg) -> int:
    return _lut_lerp(SIN_Q15, _phase_from_deg(int(deg)))

def lut_cos_deg(deg) -> int:
    return _lut_lerp(SIN_Q15, _phase_from_deg(int(deg) + 90))

def lut_sin_amp(deg, amp) -> int:
    return (lut_sin_deg(deg) * int(amp)) >> 15

class RunError(Exception):
    pass

def _strip_comments(src: str) -> str:
    out = []
    for line in src.splitlines():
        if '//' in line:
            line = line[: line.index('//')]
        out.append(line)
    return '\n'.join(out)

class Runner:
    def __init__(self):
        self.env = {}
        self.out = []
    def run(self, src: str) -> str:
        src = _strip_comments(src)
        try:
            from vulcan_latex import preprocess
            src = preprocess(src)
        except Exception:
            pass
        src = re.sub(r'set_\w+[^\n;]*;', '', src)
        self._exec_block(src)
        return ''.join(self.out)
    def _exec_block(self, src: str):
        i, n = 0, len(src)
        while i < n:
            while i < n and src[i].isspace():
                i += 1
            if i >= n:
                break
            if src.startswith('fn ', i):
                i = self._take_fn(src, i); continue
            if src.startswith('struct ', i):
                i = src.find('}', i)
                i = src.find(';', i) + 1 if i >= 0 else n
                continue
            if src.startswith('if[', i):
                i = self._exec_if(src, i); continue
            if src.startswith('do n[', i) or src.startswith('do ', i):
                i = self._exec_do(src, i); continue
            end = src.find(';', i)
            if end < 0:
                stmt, i = src[i:].strip(), n
            else:
                stmt, i = src[i:end].strip(), end + 1
            if stmt:
                self._stmt(stmt)
    def _take_fn(self, src, i):
        head = src[i:src.find('{', i)]
        m = re.search(r'fn\s+([A-Za-z_]\w*)', head)
        args = re.search(r'in\[([^\]]*)\]', head)
        end = self._skip_fn(src, i)
        if not m:
            return end
        name = m.group(1)
        params = [p.strip() for p in args.group(1).split(',') if p.strip()] if args else []
        body = src[src.find('{', i) + 1 : end]
        expr = '0'
        for line in body.split(';'):
            line = line.strip()
            if line.startswith('return '):
                expr = line[7:].strip()
        self.env['__fn_' + name] = (params, expr)
        return end
    def _skip_fn(self, src, i):
        b = src.find('{', i)
        if b < 0:
            return len(src)
        depth, j = 0, b
        while j < len(src):
            if src[j] == '{': depth += 1
            elif src[j] == '}':
                depth -= 1
                if depth == 0:
                    j += 1
                    while j < len(src) and src[j] not in ';\n':
                        j += 1
                    if j < len(src) and src[j] == ';':
                        j += 1
                    return j
            j += 1
        return len(src)
    def _exec_if(self, src, i):
        lb, rb = src.find('[', i), src.find(']', src.find('[', i))
        cond = self._eval(src[lb + 1 : rb])
        body_l = src.find('{', rb)
        body_r, nxt = self._matching_brace(src, body_l)
        body = src[body_l + 1 : body_r]
        rest = src[body_r + 1 :].lstrip()
        if rest.startswith('else'):
            el = src.find('{', body_r + 1)
            er, nxt = self._matching_brace(src, el)
            self._exec_block(body if cond else src[el + 1 : er])
            return nxt
        if cond:
            self._exec_block(body)
        return nxt
    def _exec_do(self, src, i):
        lb, rb = src.find('[', i), src.find(']', src.find('[', i))
        count = int(self._eval(src[lb + 1 : rb]))
        body_l = src.find('{', rb)
        body_r, nxt = self._matching_brace(src, body_l)
        body = src[body_l + 1 : body_r]
        for _ in range(max(0, count)):
            self._exec_block(body)
        return nxt
    def _matching_brace(self, src, l):
        depth, j = 0, l
        while j < len(src):
            if src[j] == '{': depth += 1
            elif src[j] == '}':
                depth -= 1
                if depth == 0:
                    return j, j + 1
            j += 1
        return len(src) - 1, len(src)
    def _stmt(self, stmt: str):
        if stmt.startswith('print(') and stmt.endswith(')'):
            self.out.append(str(self._eval(stmt[6:-1].strip())) + '\n'); return
        if stmt.startswith('return'): return
        if re.match(r'(?:i32|f32|bool)\s+[A-Za-z_]\w*$', stmt):
            self.env[stmt.split()[-1]] = 0; return
        m = re.match(r'(?:i32|f32|bool)?\s*([A-Za-z_]\w*)\s*=\s*(.*)$', stmt)
        if m and m.group(2) != '':
            self.env[m.group(1)] = self._eval(m.group(2)); return
        m = re.match(r'(.+)=\s*([A-Za-z_]\w*)$', stmt)
        if m:
            self.env[m.group(2)] = self._eval(m.group(1)); return
        self._eval(stmt)
    def _eval(self, expr: str):
        expr = expr.strip()
        if not expr: return 0
        if expr[0] == '"' and expr[-1] == '"': return expr[1:-1]
        mcall = re.match(r'([A-Za-z_]\w*)\s+in\[(.*?)\](?:\s+out\[[^\]]*\])?\s*$', expr)
        if mcall and ('__fn_' + mcall.group(1)) in self.env:
            params, body = self.env['__fn_' + mcall.group(1)]
            raw_args = [a.strip() for a in mcall.group(2).split(',') if a.strip()]
            local = dict(self.env)
            for n, a in zip(params, raw_args):
                local[n] = self._eval(a)
            saved, self.env = self.env, local
            try:
                return self._eval(body)
            finally:
                self.env = saved
        expr = re.sub(r'\bsin_amp\s*\(', ' _sa(', expr)
        expr = re.sub(r'\bsin\s*\(', ' _s(', expr)
        expr = re.sub(r'\bcos\s*\(', ' _c(', expr)
        expr = re.sub(r'\btan\s*\(', ' _t(', expr)
        safe = {'_s': lut_sin_deg, '_c': lut_cos_deg,
                '_t': lambda d: (lut_sin_deg(d) * 32767) // (lut_cos_deg(d) or 1),
                '_sa': lut_sin_amp}
        safe.update(self.env)
        try:
            return eval(expr, {'__builtins__': {}}, safe)
        except Exception as e:
            raise RunError(f'{expr}: {e}') from e

def run_source(src: str) -> str:
    return Runner().run(src)

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ('-h', '--help'):
        sys.stderr.write('usage: vulcan_run.py file.vul\n'); return 2
    sys.stdout.write(run_source(open(argv[0], encoding='utf-8').read()))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
