# Module graph

```
vulcan-lang                 BASE
  language, tags, examples

     +-- desktop VM         depends on BASE only
     |     vulcan_run.py
     |     vulcan_latex.py
     |
     +-- watch VM           depends on BASE only
     |     (not in this repo)
     |     OIRIA os_code/core/rs_vm
     |
     `-- Vulcan IDE         depends on BASE + desktop VM
           vulcan_ide.py
           graph_preview.py
           latex_view.py
           companion.py
```

- Neither VM depends on the IDE.
- VMs do not depend on each other.
- Watch VM is a C port of BASE, not an import of `vulcan_run`.
- OIRIA OS requires BASE and ships the watch VM.
