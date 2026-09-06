# Vulcan BASE standard

The language backend is the **C++ VM** (`rs_vm`), on watch and desktop.

Python may start that binary. It must not replace it.

## Must

- `.vul` via `rsvm_compile` / `rsvm_eval` / `rsvm_run`
- LUT `sin` `cos` `tan` `sin_amp` (degrees, wrap)
- `@latex_internal` rewrite in the C parser
- desktop host = print/stdio; watch host = GPIO/LCD
