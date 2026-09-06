#include "rs_vm.hpp"
#include "rs_vm_parse.hpp"
#include <stdio.h>
#include <string.h>
void rsvm_install_desktop_host(rsvm_t* vm);
int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: rsvm file.vul\n"); return 2; }
    rsvm_t vm; rsvm_init(&vm); rsvm_install_desktop_host(&vm);
    rsvm_parse_err_t err; memset(&err, 0, sizeof err);
    rsvm_status_t st = rsvm_eval_file(&vm, argv[1], &err);
    if (st != RSVM_OK) {
        fprintf(stderr, "%s:%d:%d %s\n", argv[1], err.line, err.column, err.message);
        return 1;
    }
    return 0;
}
