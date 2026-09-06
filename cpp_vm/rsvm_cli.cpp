#include <stdio.h>
#include <string.h>
int rsvm_eval_path(const char* path);
int main(int argc, char** argv) {
  if (argc < 2) { fprintf(stderr, "usage: rsvm file.vul\n"); return 2; }
  int st = rsvm_eval_path(argv[1]);
  if (st) fprintf(stderr, "rsvm failed %d\n", st);
  return st;
}
