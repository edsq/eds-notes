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

<!-- #region -->
# Project Management and Publishing through PDM

First, create the project directory and `cd` into it:

```bash
mkdir test_pdm_project
cd test_pdm_project
```
<!-- #endregion -->

<!-- #region -->
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

`pyenv local` creates a file `.python-version` which `pyenv` uses to redirect the command `python` to the `python3.11`.  Thus, we only need to tell pdm to use the usual `python` executable.

<!-- #region -->
### Using `conda`

Here, we'll use `conda` to get a particular python version, but we won't activate the conda environment (except to get a path to the `python` executable).  Environment management will be handled by PDM.

Get python 3.11:

```bash
conda create -y -p .conda_env python=3.11
pdm init --python ./conda_env/bin/python
```
<!-- #endregion -->
