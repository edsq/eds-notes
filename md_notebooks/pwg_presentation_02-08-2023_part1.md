---
jupyter:
  celltoolbar: Slideshow
  jupytext:
    cell_metadata_filter: all
    notebook_metadata_filter: all
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
  kernelspec:
    display_name: Bash
    language: bash
    name: bash
  language_info:
    codemirror_mode: shell
    file_extension: .sh
    mimetype: text/x-sh
    name: bash
  rise:
    autolaunch: false
    scroll: true
---

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
bind "set show-mode-in-prompt off"  # Turn off showing the vi mode in prompt, which clutters up the output here
```

<!-- #region slideshow={"slide_type": "slide"} -->
# Project Management with PDM

Part 1 of notes from talk given to the WSU Python Working Group on February 8, 2023.

Here I show the basics of project management with [PDM](https://pdm.fming.dev/latest/): how to create a project,
add dependencies, and add development dependencies.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{note}
A companion repository with the example project created in these notes is available [here](https://github.com/edsq/eeskew-pwg-test-000).
:::
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

Here, we'll use python version 3.11, but you may change this to be whatever you like.  I'll cover two methods of setting the python version: using [`pyenv`](https://github.com/pyenv/pyenv), and using [`conda`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

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
`pyenv local` creates a file `.python-version` which `pyenv` uses to redirect the command `python` to `python3.11`.  Thus, we only need to tell pdm to use the usual `python` executable.
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

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# Make sure we're in the repo directory
# Note: if cwd is already the companion repo, this will fail.
# Either restart the kernel first or don't run this cell, in that case.
project_dir=$(pdm info --where)
cd $project_dir/repos/eeskew-pwg-test-000
```

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# Start companion repo fresh from the beginning
git clean -dfx  # remove all untracked files (src, build, dist, .venv)
git checkout $(git rev-list --topo-order main | tail -1)  # check out first commit
pdm venv create --force python
```

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# This cell hidden in presentation and docs
# Check that the environment and project are correct
pdm info
```

<!-- #region slideshow={"slide_type": "slide"} -->
## The PDM project

Let's take a look at what we've created:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
ls -a
```

<!-- #region slideshow={"slide_type": "notes"} -->
The relevant files created are the `README.md`; `.pdm.toml`, which holds local configuration for this PDM project; and `pyproject.toml`, which holds project tool configuration and package metadata.

:::{seealso}
PDM has also created a virtual environment for us in the `.venv` directory.  This is where our package and its dependencies will be installed.  If you are unfamiliar with virtual environments, I recommend [this article](https://realpython.com/python-virtual-environments-a-primer/).
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### The `pyproject.toml` file
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} scrolled=false trusted=true tags=["remove-input"]
FILE="pyproject.toml"
echo "\`\`\`toml
# $FILE
$(cat $FILE)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "notes"} -->
This file is written in `.toml` format, which stands for [Tom's Obvious Minimal Language](https://toml.io/en/).

The `tool.pdm` table is empty, although we'll add things here later on.

The `project` table contains the metadata needed to install our project.  Its values thus far were set by the options we chose while running `pdm init`.

The `build-system` section tells the build frontend (e.g. `pip`) what build backend to use - the build backend is what will actually create the distribution artifacts (wheels and sdists), which we'll see later.  See [PEP 517](https://peps.python.org/pep-0517/) for more information.  Here, we're just using the default PDM backend.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on writing `pyproject.toml`](https://pdm.fming.dev/latest/pyproject/pep621/) for more on what can be specified in this file.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Adding code

First we create our package directory in [src layout](https://hynek.me/articles/testing-packaging/), with an empty (for now) `__init__.py` file to indicate that it is a python package:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
mkdir src
mkdir src/eeskew_pwg_test_000
touch src/eeskew_pwg_test_000/__init__.py
```

<!-- #region slideshow={"slide_type": "notes"} -->
:::{note}
By convention, we use [snake_case](https://en.wikipedia.org/wiki/Snake_case) for the package name, while we used [kebab-case](https://en.wiktionary.org/wiki/kebab_case) for the repository name.
:::
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

<!-- #region slideshow={"slide_type": "slide"} -->
### Add a module

Let's add some code in `src/eeskew_pwg_test_000/utils.py`:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
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

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
FILE="src/eeskew_pwg_test_000/utils.py"
echo "\`\`\`python
# $FILE
$(cat $FILE)
\`\`\`" | displayMD
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

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm install
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Now we can import our package:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run python -c 'from eeskew_pwg_test_000.utils import sarcasm; print(sarcasm("Hello world!"))'
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Note we have to type `pdm run` before our command for it to be run within our project environment.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### The `pdm.lock` file

Running `pdm install` also created a new file, `pdm.lock`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
ls
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
FILE="pdm.lock"
echo "\`\`\`toml
# $FILE
$(cat pdm.lock)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "notes"} -->
This is a lockfile, which will contain the exact versions of each project dependency we install.  It is useful for creating a perfect reproduction of the project virtual environment, which keeps our development reproducible over time and across different machines.

Right now, we have not installed anything other than the project itself, so it is essentially empty.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Add a dependency

Let's add a dependency to our project:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm add cowsay
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What did `pdm add` do?

`cowsay` now appears as a dependency in `pyproject.toml`:
<!-- #endregion -->

```bash tags=["remove-input"] slideshow={"slide_type": "fragment"} trusted=true
echo "\`\`\`toml
$(simple-diff HEAD~ pyproject.toml)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "skip"} -->
Click below to show diff:
<!-- #endregion -->

```bash slideshow={"slide_type": "notes"} trusted=true tags=["remove-input", "hide-output"]
git diff --color HEAD~ pyproject.toml | ../../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We've also updated `pdm.lock` to include cowsay:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
echo "\`\`\`toml
$(simple-diff HEAD~ pdm.lock)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We can now import `cowsay`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run python -c 'import cowsay; cowsay.cow("moo!")'
```

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on managing dependencies](https://pdm.fming.dev/latest/usage/dependency/) for more information.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Adding more code

Let's add a new function to `utils.py`:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
echo "\`\`\`python
$(simple-diff --context 0 HEAD~ src/eeskew_pwg_test_000/utils.py)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "skip"} -->
Click below to show diff:
<!-- #endregion -->

```bash slideshow={"slide_type": "notes"} tags=["remove-input", "hide-output"] trusted=true
git diff --color HEAD~ src/eeskew_pwg_test_000/utils.py | ../../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We can now run this new function:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
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

```bash slideshow={"slide_type": "fragment"} tags=["output_scroll"] scrolled=true trusted=true
pdm add -d black
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What happened?

We've added a new `[dev-dependencies]` sub-table to the `[tool.pdm]` table, which contains `black`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
echo "\`\`\`toml
$(simple-diff HEAD~ pyproject.toml)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "skip"} -->
Click below to show diff:
<!-- #endregion -->

```bash slideshow={"slide_type": "notes"} tags=["remove-input", "hide-output"] trusted=true
git diff --color HEAD~ pyproject.toml | ../../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "notes"} -->
When we run `pdm install`, by default, PDM will install dependencies from here in addition to the dependencies listed in `[project.dependencies]`.  A different tool like `pip`, however, will not.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on adding development dependencies](https://pdm.fming.dev/latest/usage/dependency/#add-development-only-dependencies) or the [PDM docs on development dependencies in `pyproject.toml`](https://pdm.fming.dev/latest/pyproject/tool-pdm/#development-dependencies) for more information on development dependencies.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
The lockfile has also been updated:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["output_scroll"] trusted=true
cat pdm.lock
```

<!-- #region slideshow={"slide_type": "notes"} -->
Many new packages now exist in the lockfile, not just `cowsay` and `black`.  This is because (unlike `cowsay`), `black` itself has dependencies that we needed to install to get it to work.  This lock file records exactly the versions of those sub-dependencies that we've now installed into our project virtual environment.

When we run `pdm install`, if the lock file exists (and `pyproject.toml` hasn't been changed since the lockfile was last updated), PDM will install precisely the packages listed in the lockfile, so we'll always be working in the same virtual environment.  This is useful for developing and testing the code, so you should always include the lockfile in your project version control.

However, we don't want to impose these restrictions on users of our library, or our project would rapidly become impossible to install due to other packages requiring different versions of the packages in the lockfile.  The only thing that we care about is that users have the right versions of the dependencies we directly use, which are listed in the `project.dependencies` array in `pyproject.toml`.  This is why `pip install` does not care about the existence of the lockfile.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on version control](https://pdm.fming.dev/latest/usage/project/#working-with-version-control) for more on best practices for version-controlling a PDM project.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Using black

We can now run `black` within our environment.  Let's re-write our code with poor formatting (note the spacing around the `==`, `%`, and `+=` operators), and then run `black` on it:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
echo "\`\`\`python
$(simple-diff --context 2 HEAD~ src/eeskew_pwg_test_000/utils.py)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "skip"} -->
Click below to show diff:
<!-- #endregion -->

```bash slideshow={"slide_type": "notes"} tags=["remove-input", "hide-output"] trusted=true
git diff --color HEAD~ src/eeskew_pwg_test_000/utils.py | ../../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "subslide"} -->
This is bad formatting!  Rather than fix it manually, we can run `black` on our code, which will auto-impose a reasonable style.
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run black src/
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What happened?
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
git diff --color HEAD~ src/eeskew_pwg_test_000/utils.py | ../../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "notes"} -->
`black` has automatically re-formatted our code, fixing the poor formatting we introduced earlier.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [black documentation](https://black.readthedocs.io/en/stable/) for more information.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Conclusion

That's all for Part 1!  The examples here should be enough to get you started using PDM to manage your own python projects.  For more advanced usage, check out the PDM documentation on:

- [General project management](https://pdm.fming.dev/latest/usage/project/)
- [Working with virtualenv](https://pdm.fming.dev/latest/usage/venv/)
- [Managing dependencies](https://pdm.fming.dev/latest/usage/dependency/)

In Part 2, we'll cover how to publish a PDM project on PyPI, so that it can be installed with a simple `pip install`.
<!-- #endregion -->
