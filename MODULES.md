# What this repo is

**vulcan-lang is BASE.** Not an IDE. Not “the watch.”

Like Java: this tree is the language + bytecode + parser + runtime *libraries*.
Both products link it.

```
vulcan-lang                    BASE  (this repo)
  C++ libs: parse, bytecode, eval rules, opcodes, LUT
  cpp_vm/ ← shared core (+ desktop host bits)

        | links BASE
        v
vulcan-ide                     DESKTOP PRODUCT
  editor + VM backend
  user runs Vulcan on Linux/Windows
  like a C# IDE sitting on the CLR

        | links BASE
        v
OIRIA watch VM                 DEVICE PRODUCT
  another VM implementation
  local ESP host (GPIO, LCD, UART)
  same bytecode/parse/rules from BASE
```

Python scripts here are glue. They are not BASE.
