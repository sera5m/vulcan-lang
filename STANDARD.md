# Vulcan BASE standard

Both VMs implement this. The IDE does not define the language.

## Must

- Source `.vul`; bytecode image optional (`.bvul`)
- Integers default; `print`, `fn name in[] out[]`, `return`
- `sin` / `cos` / `tan` / `sin_amp`: degrees, wrap `2^32` turn, Q15 256-pt LUT on constrained targets
- `@latex_internal` on a pure `fn`: body is LaTeX, rewritten to Vulcan before run
- `@sig_gen_graph_preview` is IDE-only metadata; VMs may ignore it

## Watch VM (OIRIA `os_code/core/rs_vm`)

C interpreter. Same tags and LUT contract. No Python. No IDE in the firmware link.

## Desktop VM (`vulcan_run.py` in this repo)

Python reference. Same tags and LUT contract.

## Must not

- Watch VM import `vulcan_run`
- BASE depend on vulcan-ide or OIRIA
