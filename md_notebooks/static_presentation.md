---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Bash
    language: bash
    name: bash
---

<!-- #region slideshow={"slide_type": "slide"} -->
# Project Management and Publishing through PDM

First, create the project directory and `cd` into it:

```bash
mkdir eeskew_pwg_test_project
cd eeskew_pwg_test_project
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Set the python version and initialize the project

Here, we'll use python version 3.11, but you may change this to be whatever you like.

### Using `pyenv` (recommended)

Install python 3.11 if it is not already (see installed versions with `pyenv versions`):

```bash
pyenv install 3.11
```

Set the local python version for this project and initialize using that version:

```bash
pyenv local 3.11
pdm init --python python
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
`pyenv local` creates a file `.python-version` which `pyenv` uses to redirect the command `python` to the `python3.11`.  Thus, we only need to tell pdm to use the usual `python` executable.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
### Using `conda`

Here, we'll use `conda` to get a particular python version, but we won't activate the conda environment (except to get a path to the `python` executable).  Environment management will be handled by PDM.

Get python 3.11:

```bash
conda create -y -p .conda_env python=3.11
pdm init --python ./conda_env/bin/python
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## The PDM project

Let's look at what we've created:

```bash
$ ls -a
.
..
.python-version
.pdm.toml
.venv
README.md
pyproject.toml
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### The `pyproject.toml` file

```
[tool.pdm]

[project]
name = "eeskew-pwg-test-project"
version = "0.1.0"
description = "A test project for presentation to the WSU Python Working Group."
authors = [
    {name = "Edward Eskew", email = "edward.eskew@wsu.edu"},
]
dependencies = []
requires-python = ">=3.11"
readme = "README.md"
license = {text = "MIT"}

[build-system]
requires = ["pdm-pep517>=1.0"]
build-backend = "pdm.pep517.api"
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Adding code

```bash
mkdir src
mkdir src/eeskew_pwg_test_project
touch src/eeskew_pwg_test_project/__init__.py
touch src/eeskew_pwg_test_project/main.py
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Let's add content to `main.py`:

```python
# src/eeskew_pwg_test_project/main.py

def sarcasm(s):
    """Convert string `s` to sArCaSm TeXt."""
    out = ''
    for i, c in enumerate(s):
        if i % 2 == 0:
            out += c.lower()

        else:
            out += c.upper()

    return out
```
<!-- #endregion -->
