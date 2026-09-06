/* Desktop host stubs. Link against the watch C++ VM core. */
#include <stdio.h>
#include <stdint.h>
int rsvm_eval_path(const char* path) {
  FILE* f = fopen(path, "rb");
  if (!f) return 2;
  fclose(f);
  /* When rs_vm.cpp is linked, replace this stub by calling rsvm_eval_file. */
  fprintf(stderr, "rsvm: link watch core from OIRIA_ROOT (see cpp_vm/README.md)\n");
  fprintf(stderr, "would eval %s with rs_vm C++ core\n", path);
  return 0;
}
