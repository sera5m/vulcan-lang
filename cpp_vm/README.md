BASE C++ VM for desktop and watch.

Watch already has the parse/run `.cpp` in OIRIA `os_code/core/rs_vm`.
Desktop links **those same files** plus `rsvm_host_desktop.cpp`.

```bash
cmake -S cpp_vm -B cpp_vm/build -DOIRIA_ROOT=/path/to/OIRIA_OS_espIDF
cmake --build cpp_vm/build
./cpp_vm/build/rsvm ../examples/sin_demo.vul
```
