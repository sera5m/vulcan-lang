#include "rs_vm.hpp"
#include "rs_vm_nseq.h"
#include <stdio.h>
#include <string.h>
#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif
static void p_i32(int32_t v, void*) { printf("%d\n", (int)v); }
static void p_str(const char* s, uint8_t len, void*) {
    if (s && len) fwrite(s, 1, len, stdout);
    fputc('\n', stdout);
}
static void p_char(char c, void*) { fputc(c, stdout); }
static void p_delay(uint32_t ms, void*) {
#ifdef _WIN32
    Sleep(ms);
#else
    usleep(ms * 1000u);
#endif
}
static int p_native(const char* name, const int32_t* args, int nargs,
                    int32_t* out, void*) {
    (void)args; (void)nargs;
    if (out) *out = 0;
    if (name) fprintf(stderr, "[native %s]\n", name);
    return 0;
}
static int p_nid(int nid, const int32_t* args, int nargs, int32_t* out, void*) {
    (void)args; (void)nargs;
    if (out) *out = 0;
    fprintf(stderr, "[nid %s]\n", rsvm_nid_name(nid));
    return 0;
}
void rsvm_install_desktop_host(rsvm_t* vm) {
    rsvm_host_t h; memset(&h, 0, sizeof h);
    h.print_i32 = p_i32; h.print_str = p_str; h.print_char = p_char;
    h.delay_ms = p_delay;
    h.native_call = p_native;
    h.native_id = p_nid;
    rsvm_set_host(vm, &h);
}
