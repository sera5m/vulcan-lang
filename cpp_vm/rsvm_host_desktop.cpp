#include "rs_vm.hpp"
#include <stdio.h>
#include <string.h>
static void p_i32(int32_t v, void*) { printf("%d\n", (int)v); }
static void p_str(const char* s, uint8_t len, void*) {
    if (s && len) fwrite(s, 1, len, stdout);
    fputc('\n', stdout);
}
static void p_char(char c, void*) { fputc(c, stdout); }
void rsvm_install_desktop_host(rsvm_t* vm) {
    rsvm_host_t h; memset(&h, 0, sizeof h);
    h.print_i32 = p_i32; h.print_str = p_str; h.print_char = p_char;
    rsvm_set_host(vm, &h);
}
