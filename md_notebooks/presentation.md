---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region slideshow={"slide_type": "slide"} -->
# Project Management and Publishing through PDM

First, create and `cd` into the project directory:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
cd ..
mkdir eeskew-pwg-test-project
cd eeskew-pwg-test-project
```

```python slideshow={"slide_type": "subslide"}
# We'll do this in python so that the python kernel remembers
import os
os.chdir(os.path.join('..', 'eeskew-pwg-test-project'))
```

```bash slideshow={"slide_type": "fragment"}
pwd
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Set the python version and initialize the project

Here, we'll use `conda` to get a particular python version, but we won't activate the conda environment.  Environment management will be handled by PDM.

Create a conda environment with python 3.11:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
conda create -y -p .conda_env python=3.11
```

<!-- #region slideshow={"slide_type": "subslide"} -->
## Initialize the project

```bash
$ pdm init --python .conda_env/bin/python
Creating a pyproject.toml for PDM...
Using Python interpreter: /Users/Ed/python/pwg_presentation_2023/eeskew_pwg_test_project/.conda_env/bin/python (3.11)
Would you like to create a virtualenv with /Users/Ed/python/pwg_presentation_2023/eeskew_pwg_test_project/.conda_env/bin/python? [y/n] (y):
Virtualenv is created successfully at /Users/Ed/python/pwg_presentation_2023/eeskew_pwg_test_project/.venv
Is the project a library that is installable?
A few more questions will be asked to include a project name and build backend [y/n] (n): y
Project name (eeskew_pwg_test_project):
Project version (0.1.0):
Project description (): A test project for presentation to the WSU Python Working Group.
Which build backend to use?
0. pdm-pep517
1. setuptools
2. flit-core
3. hatchling
4. pdm-backend
Please select (0):
License(SPDX name) (MIT):
Author name (Edward Eskew):
Author email (edward.eskew@wsu.edu):
Python requires('*' to allow any) (>=3.11):
Changes are written to pyproject.toml.
```
<!-- #endregion -->

```bash slideshow={"slide_type": "subslide"}
# We can't actually run pdm init, so manually initialize by copying the skeleton and creating the venv
cp -a ../resources/skeleton/ .
pdm venv create .conda_env/bin/python
```

<!-- #region slideshow={"slide_type": "slide"} -->
## The PDM project

Let's take a look at what we've created:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
ls -a
```

<!-- #region slideshow={"slide_type": "slide"} -->
## The `pyproject.toml` file
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
cat pyproject.toml
```
