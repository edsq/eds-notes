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

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
bind "set show-mode-in-prompt off"  # Turn off showing the vi mode in prompt, which clutters up the output here
```

<!-- #region slideshow={"slide_type": "slide"} -->
# Project Management and Publishing with PDM

Requirements:

- The ability to get python executables of different versions, such as with [pyenv](https://github.com/pyenv/pyenv) or [conda](https://docs.conda.io/en/latest/miniconda.html)
- [PDM](https://pdm.fming.dev/latest/) available globally
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
First, create the project directory and `cd` into it:

```bash
mkdir eeskew-pwg-test-000
cd eeskew-pwg-test-000
```

Note - because this is a throwaway test project, it is important that you give your project a name that won't conflict with any other package on PyPI or TestPyPI.  Adding your name and some numbers is a good way to ensure this.
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
pdm init --python .conda_env/bin/python
```
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
# Manually create the project
cd ..
rm -r eeskew-pwg-test-000  # remove the test project if it already exists
mkdir eeskew-pwg-test-000
cd eeskew-pwg-test-000
cp -a ../resources/skeleton/ .
pdm venv create python
```

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
# Check that the environment and project are correct
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
mkdir src/eeskew_pwg_test_000
touch src/eeskew_pwg_test_000/__init__.py
```

<!-- #region slideshow={"slide_type": "slide"} -->
### Add a module

Let's add some code in `src/eeskew_pwg_test_000/utils.py`:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
cat << "EOF" > src/eeskew_pwg_test_000/utils.py
def sarcasm(s):
    """Convert string `s` to sArCaSm TeXt."""
    out = ''
    for i, c in enumerate(s):
        if i % 2 == 0:
            out += c.lower()
        else:
            out += c.upper()
    return out
EOF
```

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/utils.py
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
pdm run python -c 'from eeskew_pwg_test_000.utils import sarcasm; print(sarcasm("Hello world!"))'
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
pdm run python -c 'import cowsay; cowsay.cow("moo!")'
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Adding more code

Let's add a new function to `utils.py`:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
cat << "EOF" > src/eeskew_pwg_test_000/utils.py
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
EOF
```

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/utils.py
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We can now run this new function:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run python -c 'from eeskew_pwg_test_000.utils import sarcastic_cowsay; sarcastic_cowsay("mooo!")'
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

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
cat << "EOF" > src/eeskew_pwg_test_000/utils.py
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
EOF
```

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/utils.py
```

```bash slideshow={"slide_type": "fragment"}
pdm run black src/
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What happened?
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/utils.py
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Package version

Right now, the package version (`"0.1.0"`) is stored in the `pyproject.toml` file (in the `project.version` keyword).  The best practice is to place this in a `__version__.py` file, and have that be the single source of truth for our package version.

Create a `__version__.py` file in `src/eeskew_pwg_test_000`, and add the `__version__` variable to it.  The new file should look like:
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# This cell hidden in presentation and docs
echo '__version__ = "0.1.0"' > src/eeskew_pwg_test_000/__version__.py
```

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/__version__.py
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Now modify the `pyproject.toml` file so that the version is [dynamic metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#dynamic):
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# This cell hidden in presentation and docs
cat << EOF > pyproject.toml
[tool.pdm]
version = { source = "file", path = "src/eeskew_pwg_test_000/__version__.py" }

[tool.pdm.dev-dependencies]
dev = [
    "black>=23.1.0",
]

[project]
name = "eeskew-pwg-test-000"
description = "A test project for presentation to the WSU Python Working Group."
authors = [
    {name = "Edward Eskew", email = "edward.eskew@wsu.edu"},
]
dependencies = [
    "cowsay>=5.0",
]
requires-python = ">=3.11"
readme = "README.md"
license = {text = "MIT"}
dynamic = ["version"]

[build-system]
requires = ["pdm-pep517>=1.0"]
build-backend = "pdm.pep517.api"
EOF
```

```bash slideshow={"slide_type": "fragment"}
cat pyproject.toml
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Note the new `project.dynamic` array, the new `tool.pdm.version` table, and that the `project.version` key is gone.
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm show --version
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We should also add the `__version__` variable to our `__init__.py`:
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# This cell hidden in presentation and docs
echo 'from eeskew_pwg_test_000.__version__ import __version__' > src/eeskew_pwg_test_000/__init__.py
```

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/__init__.py
```

<!-- #region slideshow={"slide_type": "fragment"} -->
This allows us to check the version from python in the conventional way:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run python -c "import eeskew_pwg_test_000; print(eeskew_pwg_test_000.__version__)"
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Packaging the project

Let's review the project as it exists so far:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
tree
```

<!-- #region slideshow={"slide_type": "subslide"} -->
To create a [sdist](https://packaging.python.org/en/latest/specifications/source-distribution-format/) and [wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/):
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm build
```

<!-- #region slideshow={"slide_type": "slide"} -->
### What happened?

We've created a new directory named `dist`, where these two distribution formats have been placed.
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
tree
```

<!-- #region slideshow={"slide_type": "fragment"} -->
We could install this project into a different python environment with `python -m pip install dist/eeskew-pwg-test-000-0.1.0.tar.gz` or `python -m pip install dist/eeskew_pwg_test_000-0.1.0-py3-none-any.whl` (the latter is faster).
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Publishing the project

Now we'll publish the project on (Test)PyPI.

0. First, make an account on [TestPyPI](https://test.pypi.org).
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
1. Navigate to your account settings, scroll down to "API tokens", and click "Add API token"
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
2. Give the token a descriptive name, set the scope to "Entire account (all projects)", and click "Add token".
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
3. Copy the token that appears - heeding the warning that it will appear only once!
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
4. Now we'll configure PDM with these credentials (replacing `<PASTE_YOUR_TOKEN_HERE>` with the token you've just copied:

```bash
pdm config repository.testpypi.username "__token__"
pdm config repository.testpypi.password "<PASTE_YOUR_TOKEN_HERE>"
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
5. Finally, to publish on TestPyPI, just run

```bash
pdm publish -r testpypi
```

Note that you do not need to run `pdm build` first - PDM will build the distribution as part of `publish` anyway.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Updating your project

Let's add an entrypoint for our project in `pyproject.toml`.  First, add a new module and new function:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
cat << "EOF" > src/eeskew_pwg_test_000/cli.py
import argparse

from eeskew_pwg_test_000.utils import sarcastic_cowsay

def main():
    """Cowsay something sarcastically from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("speech")
    args = parser.parse_args()
    
    s = args.speech
    sarcastic_cowsay(s)
EOF
```

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/cli.py
```

<!-- #region slideshow={"slide_type": "slide"} -->
Now let's add the script to `pyproject.toml`:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
cat << "EOF" > pyproject.toml
[tool.pdm]
version = { source = "file", path = "src/eeskew_pwg_test_000/__version__.py" }

[tool.pdm.dev-dependencies]
dev = [
    "black>=23.1.0",
]

[project]
name = "eeskew-pwg-test-000"
description = "A test project for presentation to the WSU Python Working Group."
authors = [
    {name = "Edward Eskew", email = "edward.eskew@wsu.edu"},
]
dependencies = [
    "cowsay>=5.0",
]
requires-python = ">=3.11"
readme = "README.md"
license = {text = "MIT"}
dynamic = ["version"]

[project.scripts]
sarcasticow = "eeskew_pwg_test_000.cli:main"

[build-system]
requires = ["pdm-pep517>=1.0"]
build-backend = "pdm.pep517.api"
EOF
```

```bash slideshow={"slide_type": "fragment"}
cat pyproject.toml
```

```bash slideshow={"slide_type": "subslide"}
pdm install
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Now we can run our command from within the environment:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run sarcasticow "I'm a sarcastic cow"
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Updating README

Let's update our README to show this usage:
<!-- #endregion -->

````bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
cat << "EOF" > README.md
# eeskew-pwg-test-000

Command-line usage:

```
$ sarcasticow "I'm a sarcastic cow"

  ___________________
| i'm a sArCaStIc cOw |
  ===================
                   \
                    \
                      ^__^
                      (oo)\_______
                      (__)\       )\/\
                          ||----w |
                          ||     ||

```
EOF
````

```bash slideshow={"slide_type": "fragment"}
cat README.md
```

<!-- #region slideshow={"slide_type": "slide"} -->
Now we can bump the version and publish again to TestPyPI:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
echo '__version__ = "0.2.0"' > src/eeskew_pwg_test_000/__version__.py
```

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/__version__.py
```

<!-- #region slideshow={"slide_type": "fragment"} -->
```bash
pdm publish -r testpypi
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Conclusion

And that's it!  We've gone through the basics of project management, packaging, and publishing on (Test)PyPI.
<!-- #endregion -->
