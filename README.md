# vulcan-lang

Desktop Vulcan: language runner + GTK IDE. **Not** the ESP32 watch firmware.

Watch OS: https://github.com/sera5m/OIRIA_OS_espIDF
Package index: https://github.com/sera5m/oiria-index

## Pieces

| file | what |
|------|------|
| `vulcan_run.py` | interpreter (LUT sin/cos, fns, `@latex_internal`) |
| `vulcan_latex.py` | LaTeX body → Vulcan |
| `vulcan_ide.py` | GTK4 editor, graphs, companion |
| `graph_preview.py` | `@sig_gen_graph_preview` plots |
| `companion.py` | capability-limited offload host |
| `examples/` | `.vul` samples |

`vulcan_run.py` is plain Python. Use it in other projects with no GTK.

```bash
python3 vulcan_run.py examples/sin_demo.vul
python3 -c "from vulcan_run import run_source; print(run_source('print(sin(90));'))"
```

## Linux

```bash
sudo pacman -S python python-gobject gtk4 python-pyserial python-matplotlib
python3 vulcan_ide.py examples/sig_gen.vul
```

## Windows

Interpreter:

```bat
py -3 vulcan_run.py examples\sin_demo.vul
```

IDE: MSYS2 UCRT64 GTK4 + PyGObject. GDK uses Win32 (no Wayland).

## Tags

- `@latex_internal` — body is LaTeX, rewritten before run
- `@sig_gen_graph_preview` — Debugger / Graphs
