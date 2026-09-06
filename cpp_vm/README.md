# C++ VM (the real one)

This is the same interpreter as the watch (`os_code/core/rs_vm`).
Python `vulcan_run.py` is only a launcher / fallback.

## Get the proven sources

They still live in OIRIA until you copy them here:

```bash
export OIRIA_ROOT=/path/to/OIRIA_OS_espIDF
cmake -S cpp_vm -B cpp_vm/build -DOIRIA_ROOT=$OIRIA_ROOT
cmake --build cpp_vm/build
./cpp_vm/build/rsvm examples/sin_demo.vul
```

Or copy:

```bash
cp -a $OIRIA_ROOT/os_code/core/rs_vm cpp_vm/rs_vm
```

Then CMake uses `cpp_vm/rs_vm` if `OIRIA_ROOT` is unset.

Host differs by target:
- watch: `rs_vm_host_esp.cpp`
- desktop: `rsvm_host_desktop.cpp` (this folder)
Core parse/run/opcodes stay shared.
