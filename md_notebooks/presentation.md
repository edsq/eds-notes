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

<!-- #region slideshow={"slide_type": "skip"} -->
### Documentation implementation

The following commands will be equivalent to the above, but work when run from inside the documentation.
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"}
cd ..
rm -r eeskew-pwg-test-project  # remove the test project if it already exists
mkdir eeskew-pwg-test-project
cd eeskew-pwg-test-project
cp -a ../resources/skeleton/ .
pdm venv create python
```

```python slideshow={"slide_type": "skip"}
# Change directory in python so that the python kernel remembers
import os
os.chdir(os.path.join('..', 'eeskew-pwg-test-project'))
```

```bash slideshow={"slide_type": "skip"}
pdm info
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

<!-- #region slideshow={"slide_type": "slide"} -->
## Adding code
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
mkdir src
mkdir src/eeskew_pwg_test_project
touch src/eeskew_pwg_test_project/__init__.py
```

<!-- #region slideshow={"slide_type": "slide"} -->
### Add a module

Let's add some code in `src/eeskew_pwg_test_project/utils.py`:
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
%%writefile src/eeskew_pwg_test_project/utils.py

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

<!-- #region slideshow={"slide_type": "slide"} -->
## Install the project
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm install
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Now we can import our package:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run python -c "from eeskew_pwg_test_project.utils import sarcasm; print(sarcasm('Hello world!'))"
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Note we have to type `pdm run` before our command for it to be run within our project environment.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Add a dependency

Let's add a dependency to our project:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}

pdm add cowsay
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What did `pdm add` do?

`cowsay` now appears as a dependency in `pyproject.toml`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
cat pyproject.toml
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We can now also import `cowsay`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run python -c "import cowsay; cowsay.cow('moo!')"
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Adding more code

Let's add a new function to `utils.py`:
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
%%writefile src/eeskew_pwg_test_project/utils.py
import cowsay

def sarcasm(s):
    """Convert string `s` to sArCaSm TeXt."""
    out = ""
    for i, c in enumerate(s):
        if i % 2 == 0:
            out += c.lower()

        else:
            out += c.upper()

    return out

def sarcastic_cowsay(s):
    """Cowsay `s`, sArCaStIcAlLy."""
    sarcastic_s = sarcasm(s)
    cowsay.cow(sarcastic_s)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We can now run this new function:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run python -c "from eeskew_pwg_test_project.utils import sarcastic_cowsay; sarcastic_cowsay('mooo!')"
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Add a development dependency

The dependencies listed in the `project.dependencies` section of `pyproject.toml` will all be installed when someone runs `pip install eeskew_pwg_test_project`.  What if we have dependencies we only want in our development environment?

Let's add `black`, a tool to automatically format our code:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm add -d black
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What happened?
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
cat pyproject.toml
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Using black

We can now run `black` within our environment.  Let's re-write our code with poor formatting (note the spacing around the `==`, `%`, and `+=` operators), and then run `black` on it:
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
%%writefile src/eeskew_pwg_test_project/utils.py
import cowsay

def sarcasm(s):
    """Convert string `s` to sArCaSm TeXt."""
    out = ''
    for i,c in enumerate(s):
        if i% 2 ==0:
            out +=c.lower()

        else:
            out+= c.upper()

    return out

def sarcastic_cowsay(s):
    """Cowsay `s`, sArCaStIcAlLy."""
    sarcastic_s = sarcasm(s)
    cowsay.cow(sarcastic_s)
```

```bash slideshow={"slide_type": "fragment"}
pdm run black src/
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What happened?
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_project/utils.py
```
