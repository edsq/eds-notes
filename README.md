# Ed's Notes: Physics, Math, and Python

[![Jupyter Book Badge](https://jupyterbook.org/badge.svg)](https://edsq.github.io/eds-notes/intro.html)

Notes on miscellaneous topics in physics, math, and python.

Available as a Jupyter Book [here](https://edsq.github.io/eds-notes/intro.html).

## Installing

1. Install the package:
```
pdm install
```

2. Install the Jupyter bash kernel:
```
pdm run python -m bash_kernel.install
```

3. Generate the notebooks from synced markdown files using `jupytext`:
```
pdm run jupytext --sync md_notebooks/*
```

4. (If you intend to commit to the repository) Install pre-commit hooks:
```
pdm run pre-commit install
```
