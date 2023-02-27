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

Notes from talk given to the WSU Python Working Group on February 8, 2023.

Here I show how to create a basic project with [PDM](https://pdm.fming.dev/latest/),
add dependencies and development dependencies, and publish the package on (Test)PyPI.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Requirements:

- The ability to get python executables of different versions, such as with [pyenv](https://github.com/pyenv/pyenv) or [conda](https://docs.conda.io/en/latest/miniconda.html)
- [PDM](https://pdm.fming.dev/latest/) available globally
- The [pdm-bump](https://github.com/carstencodes/pdm-bump) plugin installed
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
First, create the project directory and `cd` into it:

```bash
mkdir eeskew-pwg-test-000
cd eeskew-pwg-test-000
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "notes"} -->
:::{important}
Because this is a throwaway test project, it is important that you give your project a name that won't conflict with any other package on PyPI or TestPyPI. Adding your name and some numbers is a good way to ensure this.
:::
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

<!-- #region slideshow={"slide_type": "subslide"} -->
### Using `conda`

Here, we'll use `conda` to get a particular python version, but we won't activate the conda environment (except to get a path to the `python` executable).  Environment management will be handled by PDM.

Get python 3.11:

```bash
conda create -y -p .conda_env python=3.11
pdm init --python .conda_env/bin/python
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### `pdm init` options

For

```
Is the project a library that is installable?
A few more questions will be asked to include a project name and build backend [y/n] (n):
```

select `y`.  Otherwise, all the default options should be good.
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# This cell hidden in presentation and docs
cd ../eeskew-pwg-test-000
git clean -dfx  # remove all untracked files (src, build, dist, .venv)
git checkout $(git rev-list --topo-order main | tail -1)  # check out first commit
pdm venv create --force python
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

<!-- #region slideshow={"slide_type": "notes"} -->
The relevant files created are the `README.md`; `.pdm.toml`, which holds local configuration for this PDM project; and `pyproject.toml`, which holds project tool configuration and package metadata.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### The `pyproject.toml` file
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
cat pyproject.toml
```

<!-- #region slideshow={"slide_type": "notes"} -->
This file is written in `.toml` format, which stands for [Tom's Obvious Minimal Language](https://toml.io/en/).

The `tool.pdm` table is empty, although we'll add things here later on.

The `project` table contains the metadata needed to install our project.  Its values thus far were set by the options we chose while running `pdm init`.

The `build-system` section tells the build frontend (e.g. `pip`) what build backend to use - the build backend is what will actually create the distribution artifacts (wheels and sdists), which we'll see later.  See [PEP 517](https://peps.python.org/pep-0517/) for more information.  Here, we're just using the default PDM backend.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Adding code

First we create our package directory in [src layout](https://hynek.me/articles/testing-packaging/), with an empty (for now) `__init__.py` file to indicate that it is a python package:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
mkdir src
mkdir src/eeskew_pwg_test_000
touch src/eeskew_pwg_test_000/__init__.py
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
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
    out = ""
    for i, c in enumerate(s):
        if i % 2 == 0:
            out += c.lower()

        else:
            out += c.upper()

    return out
EOF
```

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"}
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"}
cat src/eeskew_pwg_test_000/utils.py
```

<!-- #region slideshow={"slide_type": "notes"} -->
The actual content of this code is not too important for the purposes of these notes, but for completeness, all it does is capitalize and lowercase alternating letters in a string.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Install the project
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "notes"} -->
To make our code available in the virtual environment, we have to install it:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm install
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
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

<!-- #region slideshow={"slide_type": "subslide"} -->
### The `pdm.lock` file

Running `pdm install` also created a new file, `pdm.lock`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
ls
```

```bash slideshow={"slide_type": "fragment"}
cat pdm.lock
```

<!-- #region slideshow={"slide_type": "notes"} -->
This is a lockfile, which will contain the exact versions of each project dependency we install.  It is useful for creating a perfect reproduction of the project virtual environment, which keeps our development reproducible over time and across different machines.

Right now, we have not installed anything other than the project itself, so it is essentially empty.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Add a dependency

Let's add a dependency to our project:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm add cowsay
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What did `pdm add` do?

`cowsay` now appears as a dependency in `pyproject.toml`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We've also updated `pdm.lock` to include cowsay:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
cat pdm.lock
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We can now import `cowsay`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run python -c 'import cowsay; cowsay.cow("moo!")'
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Adding more code

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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ src/eeskew_pwg_test_000/utils.py | ../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We can now run this new function:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run python -c 'from eeskew_pwg_test_000.utils import sarcastic_cowsay; sarcastic_cowsay("mooo!")'
```

<!-- #region slideshow={"slide_type": "notes"} -->
:::{note}
We didn't have to re-run `pdm install` to use our new function - this is because PDM installs our `eeskew_pwg_test_000` package in "editable mode", which acts sort of like a symlink between the source code and the installed files in the `.venv` directory.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Add a development dependency

The dependencies listed in the `project.dependencies` section of `pyproject.toml` will all be installed when someone runs `pip install eeskew_pwg_test_project`.  What if we have dependencies we only want in our development environment?

Let's add `black`, a tool to automatically format our code:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["output_scroll"]
pdm add -d black
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What happened?
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "notes"} -->
We've added a new `[dev-dependencies]` sub-table to the `[tool.pdm]` table.  When we run `pdm install`, by default, PDM will install dependencies from here in addition to the dependencies listed in `[project.dependencies]`.  A different tool like `pip`, however, will not.

See the [PDM docs](https://pdm.fming.dev/latest/usage/dependency/#add-development-only-dependencies) for more information on development dependencies.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
The lockfile has also been updated:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["output_scroll"]
cat pdm.lock
```

<!-- #region slideshow={"slide_type": "notes"} -->
Many new packages now exist in the lockfile, not just `cowsay` and `black`.  This is because (unlike `cowsay`), `black` itself has dependencies that we needed to install to get it to work.  This lock file records exactly the versions of those sub-dependencies that we've now installed into our project virtual environment.

When we run `pdm install`, if the lock file exists (and `pyproject.toml` hasn't been changed since the lockfile was last updated), PDM will install precisely the packages listed in the lockfile, so we'll always be working in the same virtual environment.  This is useful for developing and testing the code, so you should always include the lockfile in your project version control.

However, we don't want to impose these restrictions on users of our library, or our project would rapidly become impossible to install due to other packages requiring different versions of the packages in the lockfile.  The only thing that we care about is that users have the right versions of the dependencies we directly use, which are listed in the `project.dependencies` array in `pyproject.toml`.  This is why `pip install` does not care about the existence of the lockfile.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Using black

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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ src/eeskew_pwg_test_000/utils.py | ../scripts/diff-so-fancy
```

```bash slideshow={"slide_type": "fragment"}
pdm run black src/
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What happened?
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ src/eeskew_pwg_test_000/utils.py | ../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "notes"} -->
`black` has automatically re-formatted our code, fixing the poor formatting we introduced earlier.  See the [black documentation](https://black.readthedocs.io/en/stable/) for more information.
<!-- #endregion -->

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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Note the new `project.dynamic` array, the new `tool.pdm.version` table, and that the `project.version` key is gone.

We can check our current version like so:
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ src/eeskew_pwg_test_000/__init__.py | ../scripts/diff-so-fancy
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
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{note}
To publish on the actual index (PyPI, not TestPyPI), simply replace `testpypi` with `pypi` in the instructions that follow.  Try not to pollute PyPI with throwaway projects!
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
### Setting up PyPI credentials

0. First, make an account on [TestPyPI](https://test.pypi.org).
1. Navigate to your account settings, scroll down to "API tokens", and click "Add API token"
2. Give the token a descriptive name, set the scope to "Entire account (all projects)", and click "Add token".
3. Copy the token that appears - heeding the warning that it will appear only once!
4. Now we'll configure PDM with these credentials (replacing `<PASTE_YOUR_TOKEN_HERE>` with the token you've just copied):

```bash
pdm config repository.testpypi.username "__token__"
pdm config repository.testpypi.password "<PASTE_YOUR_TOKEN_HERE>"
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Setting up a test-publish PDM script

To publish on PyPI, we could now simply run:

```bash
pdm publish -r testpypi
```

Note that you do not need to run `pdm build` first - PDM will build the distribution as part of `publish` anyway.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
However, TestPyPI won't let you overwrite an existing version of your package, so we have to bump our version every time we want to do this.  Let's set up a PDM script to automate that.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{attention}
If you are publishing on PyPI (*not* TestPyPI), you probably don't want to use this script.  Publishing will be as simple as running `pdm bump {version}` to increment your package version number (for example, `pdm bump patch`), and then publishing with `pdm publish` (equivalent to `pdm publish -r pypyi`).
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
First, ensure you have the [pdm-bump](https://github.com/carstencodes/pdm-bump) plugin installed.

We add a new PDM script in the `tool.pdm.scripts` table of `pyproject.toml`:
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# This cell hidden in presentation and docs
cat << "EOF" > pyproject.toml
[tool.pdm]
version = { source = "file", path = "src/eeskew_pwg_test_000/__version__.py" }

[tool.pdm.scripts]
test-publish.shell = '''\
VERSION=$(pdm show --version)
pdm bump patch > /dev/null
DEV_VERSION=$(pdm show --version).dev$(date +%s)
echo "__version__ = \"$DEV_VERSION\"" > src/eeskew_pwg_test_000/__version__.py
pdm publish -r testpypi
echo "__version__ = \"$VERSION\"" > src/eeskew_pwg_test_000/__version__.py
'''

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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash tags=["remove-input"] slideshow={"slide_type": "subslide"}
git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "subslide"} -->
When we run `pdm run test-publish`, this script:
1. Gets the current version with `pdm show --version`
2. Changes the package version to a patch bump of that version with `.dev{date in seconds}` appended.  This is a [developmental release](https://peps.python.org/pep-0440/#developmental-releases) format.
3. Publishes the package on TestPyPI
4. Returns the package version to its original value

Let's run it!
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run test-publish
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Add an entrypoint to the package

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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
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

[tool.pdm.scripts]
test-publish.shell = '''\
VERSION=$(pdm show --version)
pdm bump patch > /dev/null
DEV_VERSION=$(pdm show --version).dev$(date +%s)
echo "__version__ = \"$DEV_VERSION\"" > src/eeskew_pwg_test_000/__version__.py
pdm publish -r testpypi
echo "__version__ = \"$VERSION\"" > src/eeskew_pwg_test_000/__version__.py
'''

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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy
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

<!-- #region slideshow={"slide_type": "notes"} -->
:::{note}
Because we're using `pdm` for environment management, we still need to use `pdm run` to access the script installed into the virtual environment.

Unlike the `test-publish` PDM script we wrote earlier, if we activated the environment with `source .venv/bin/activate`, we could simply use the `sarcasticow` command by itself, and users who install our package with `pip` into their own virtualenv or conda environment will also have access to `sarcasticow`.  Even better, users who install our package through [`pipx`](https://pypa.github.io/pipx/) will be able to use the `sarcasticow` command without activating a virtual environment.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Updating README

Thus far, we've left our README as an empty file.  This is bad.  Let's update it to show our utility's usage:
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"]
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"]
git diff HEAD~ README.md | ../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "slide"} -->
Finally, we publish again to TestPYPI:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
pdm run test-publish
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Our page on TestPyPI now shows the README, so users can see relevant package information before they install it.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Conclusion

And that's it!  We've gone through the basics of project management, packaging, and publishing on (Test)PyPI.
<!-- #endregion -->
