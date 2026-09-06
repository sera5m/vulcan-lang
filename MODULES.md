# Module graph

```
vulcan-lang BASE
  C++ VM core     THE interpreter (same as watch)
  cpp_vm/         desktop host + rsvm CLI
  vulcan_run.py   launcher / fallback only

     +-- vulcan-ide     starts rsvm (Python may wrap it)
     `-- OIRIA watch    same C++ core, ESP host hooks
```

Python is not the language backend.
