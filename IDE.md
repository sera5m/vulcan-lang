GTK IDE sources (`vulcan_ide.py`, `latex_view.py`, `graph_preview.py`, `companion.py`, `vulcan_latex.py`) ship from the same desktop tree used while developing with the watch.

On a machine that already has that folder:

```
cp -a /path/to/vulcan_ide/*.py .
python3 vulcan_ide.py examples/sig_gen.vul
```

`vulcan_run.py` in this repo is enough to embed Vulcan in other desktop projects.
