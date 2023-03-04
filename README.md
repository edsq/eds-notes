# Ed's Notes: Physics, Math, and Python

[![Jupyter Book Badge](https://jupyterbook.org/badge.svg)](https://edsq.github.io/eds-notes/intro.html)

Notes on miscellaneous topics in physics, math, and python.

Available as a Jupyter Book [here](https://edsq.github.io/eds-notes/intro.html).


## Installing

To install for running notebooks and building docs:

```
make init
```

This requires [PDM](https://pdm.fming.dev/latest/).

Notebooks should run when this project is installed with any PEP 517 compatible build
backend, however.  You will still need to run `jupytext --sync md_notebooks/*` to get
the actual `.ipynb` files.


## Building and publishing documentation

Build docs:

```
pdm build-docs
```

Publish docs online:

```
pdm publish-docs
```
