---
jupyter:
  celltoolbar: Tags
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# Run startup commands
# Note: if cwd is already the companion repo, this will fail.
# Either restart the kernel first or don't run this cell, in that case.
project_dir=$(pdm info --where)
source $project_dir/.bashnbrc
```

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# Make sure we're in the repo directory
GITHUB_URL='https://github.com/edsq/eeskew-pwg-test-000'  # needed for embed-repo-link
tmp_dir="_tmp_pwg_presentation_02-08-2023_part1"
repo_name="eeskew-pwg-test-000"
cd $project_dir/repos &&
rm -rf $tmp_dir &&
mkdir -p $tmp_dir/$repo_name
git clone $repo_name $tmp_dir/$repo_name &&
cd $tmp_dir/$repo_name
```

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# Start companion repo fresh from the beginning
git checkout $(git rev-list --topo-order main | tail -1)  # check out first commit
pdm venv create --force python
```

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# This cell hidden in presentation and docs
# Check that the environment and project are correct
pdm info
```

<!-- #region slideshow={"slide_type": "slide"} -->
# Project Management with PDM

Part 1 of notes from talk given to the WSU Python Working Group on February 8, 2023.  See Part 2 [here](part2.ipynb).

In this chapter, I show the basics of project management with [PDM](https://pdm.fming.dev/latest/): how to create a project,
add dependencies, and add development dependencies.

This tutorial is primarily aimed at macOS and Linux users, although the commands for Windows should mostly translate.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{note}
A companion repository with the example project created in these notes is available [here](https://github.com/edsq/eeskew-pwg-test-000).
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Requirements

- The ability to get python executables of different versions, such as with [pyenv](https://github.com/pyenv/pyenv) or [conda](https://docs.conda.io/en/latest/miniconda.html)
- [PDM](https://pdm.fming.dev/latest/) available globally
- The [pdm-bump](https://github.com/carstencodes/pdm-bump) plugin installed
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
The version of PDM these notes use is:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm --version
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Set the python version and initialize the project

First, create the project directory and `cd` into it:

```
mkdir eeskew-pwg-test-000
cd eeskew-pwg-test-000
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "notes"} -->
:::{important}
Because this is a throwaway test project, it is important that you give your project a name that won't conflict with any other package on PyPI or TestPyPI. Adding your name and some numbers is a good way to ensure this.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Here, we'll use python version 3.11, but you may change this to be whatever you like.  I'll cover two methods of setting the python version: using [`pyenv`](https://github.com/pyenv/pyenv), and using [`conda`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} tags=["remove-cell"] -->
### Using `pyenv`

Install python 3.11 if it is not already (see installed versions with `pyenv versions`):

```
pyenv install 3.11
```

Set the local python version for this project and initialize using that version:

```
pyenv local 3.11
pdm init --python python
```

`pyenv local` creates a file `.python-version`, which `pyenv` reads and redirects the command `python` to the installed `python3.11`.  Thus, we only need to tell pdm to use the usual `python` executable.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} tags=["remove-cell"] -->
### Using `conda`

PDM can also use `conda` to create your virtual environment.  To do this simply, we create the virtual environment before initializing the project, so that we can pass the right python executable to `pdm init`.

```
pdm venv create -w conda 3.11
pdm init --python .venv/bin/python
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
::::{tab-set}
:::{tab-item} Using `pyenv`

Install python 3.11 if it is not already (see installed versions with `pyenv versions`):

```
pyenv install 3.11
```

Set the local python version for this project and initialize using that version:

```
pyenv local 3.11
pdm init --python python
```

`pyenv local` creates a file `.python-version`, which `pyenv` reads and redirects the command `python` to the installed `python3.11`.  Thus, we only need to tell pdm to use the usual `python` executable.
:::

:::{tab-item} Using `conda`

PDM can use `conda` to create your virtual environment.  To do this simply, we create the virtual environment before initializing the project, so that we can pass the right python executable to `pdm init`.

```
pdm venv create -w conda 3.11
pdm init --python .venv/bin/python
```
:::
::::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### `pdm init` options

For

```
Would you like to create a virtualenv with <path-to-python>? [y/n] (y):
```

Ensure you select `y`.  Otherwise, PDM will operate in "PEP 582 mode" - see note on this below.

For

```
Is the project a library that is installable?
If yes, we will need to ask a few more questions to include the project name and build backend [y/n] (n):
```

select `y`.  Otherwise, all the default options should be good, except where you want to fill in your own information (project description, email, etc).
<!-- #endregion -->

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

<!-- #region slideshow={"slide_type": "skip"} -->
:::{note}
PDM supports the rejected Python Enhancement Proposal (PEP) [582](https://peps.python.org/pep-0582/).  An alternative to virtual environments, PEP 582 would automatically get dependencies from a `__pypackages__` directory in the project root, without having to activate a virtualenv.  See the PDM docs on PEP 582 [here](https://pdm.fming.dev/latest/usage/pep582/).  We will not be using PEP 582 mode in this tutorial.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### The `pyproject.toml` file
<!-- #endregion -->

```bash tags=["remove-input"] slideshow={"slide_type": "fragment"} trusted=true
embed-repo-link "The central location of our project configuration is {pyproject.toml}":
```

```bash slideshow={"slide_type": "fragment"} scrolled=false trusted=true tags=["remove-input"]
simple-diff $EMPTY_TREE pyproject.toml | show-code toml
```

<!-- #region slideshow={"slide_type": "notes"} -->
This file is written in `.toml` format, which stands for [Tom's Obvious Minimal Language](https://toml.io/en/).

The `tool.pdm` table is empty, although we'll add things here later on.

The `project` table contains the metadata needed to install our project.  Its values thus far were set by the options we chose while running `pdm init`.

The `build-system` section tells the build frontend (e.g. `pip`) what build backend to use - the build backend is what will actually create the distribution artifacts (wheels and sdists), which we'll see later.  See [PEP 517](https://peps.python.org/pep-0517/) for more information.  Here, we're just using the default PDM backend.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on writing `pyproject.toml`](https://pdm.fming.dev/latest/reference/pep621/) for more on what can be specified in this file.
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git-checkpoint
```

<!-- #region slideshow={"slide_type": "notes"} -->
:::{note}
By convention, we use [snake_case](https://en.wikipedia.org/wiki/Snake_case) for the package name, while we use [kebab-case](https://en.wiktionary.org/wiki/kebab_case) for the repository name.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
### Add a module
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# This cell hidden in presentation and docs
cat << "EOF" > src/eeskew_pwg_test_000/sarcasm.py
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
git-checkpoint
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
embed-repo-link "Let's add some code in {src/eeskew_pwg_test_000/sarcasm.py}:"
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
simple-diff HEAD~ src/eeskew_pwg_test_000/sarcasm.py | show-code python
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
git-checkpoint
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Now we can import our package:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run python -c 'from eeskew_pwg_test_000.sarcasm import sarcasm; print(sarcasm("Hello world!"))'
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Note we have to type `pdm run` before our command for it to be run within our project environment.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
:::{tip}
If you don't want to type `pdm run` every time before a command to be run in the project virtual environment, you can *activate* the environment, which will modify your `sys.prefix` to point to the `.venv` directory.  See the python `venv` docs [here](https://docs.python.org/3/library/venv.html#how-venvs-work) for more on how virtual environments work.

`pdm` will print the command to activate the project virtual environment with the command `pdm venv activate`.  You can copy and paste that output, or, if you want to activate the environment in one line, use:

```bash
eval $(pdm venv activate)
```

To simplify things further, add this as an alias to your `~/.bashrc` or `~/.bash_profile` (and don't forget to restart your shell or `source ~/.bashrc` after):

```bash
# ~/.bashrc
alias pdm-activate='eval $(pdm venv activate)'
```

This will let you activate the environment with the command `pdm-activate`.

You can deactivate an active virtual environment with the command `deactivate`.  See also the [PDM docs on virtualenv activation](https://pdm.fming.dev/latest/usage/venv/#activate-a-virtualenv).
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### The `pdm.lock` file

Running `pdm install` also created a new file, `pdm.lock`:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
ls
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
simple-diff HEAD~ pdm.lock | show-code toml
```

<!-- #region slideshow={"slide_type": "notes"} -->
This is a lockfile, which will contain the exact versions of each project dependency we install.  It is useful for creating a perfect reproduction of the project virtual environment, which keeps our development reproducible over time and across different machines.

Right now, we have not installed anything other than the project itself, so it is essentially empty.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Add a dependency

Let's add a dependency to our project, [cowsay](https://pypi.org/project/cowsay/):
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm add cowsay
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git-checkpoint
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What did `pdm add` do?
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
embed-repo-link "\`cowsay\` now appears as a dependency in {pyproject.toml}:"
```

```bash tags=["remove-input"] slideshow={"slide_type": "fragment"} trusted=true
simple-diff HEAD~ pyproject.toml | show-code toml
```

```bash slideshow={"slide_type": "subslide"} tags=["remove-input"] trusted=true
embed-repo-link "We've also updated {pdm.lock} to include cowsay:"
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
simple-diff HEAD~ pdm.lock | show-code toml
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
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# This cell hidden in presentation and docs
cat << "EOF" > src/eeskew_pwg_test_000/sarcasm.py
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
git-checkpoint
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
embed-repo-link "Let's add a new function to {src/eeskew_pwg_test_000/sarcasm.py}:"
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
simple-diff --context 0 HEAD~ src/eeskew_pwg_test_000/sarcasm.py | show-code python
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We can now run this new function:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run python -c 'from eeskew_pwg_test_000.sarcasm import sarcastic_cowsay; sarcastic_cowsay("mooo!")'
```

<!-- #region slideshow={"slide_type": "notes"} -->
:::{note}
We didn't have to re-run `pdm install` to use our new function - this is because PDM installs our `eeskew_pwg_test_000` package in "editable mode", which acts sort of like a symlink between the source code and the installed files in the `.venv` directory.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Add a development dependency

The dependencies listed in the `project.dependencies` section of `pyproject.toml` will all be installed when someone runs `pip install eeskew-pwg-test-000`.  What if we have dependencies we only want in our development environment?

Let's add `black`, a tool to automatically format our code:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["output_scroll"] scrolled=true trusted=true
pdm add -d black
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git-checkpoint
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What did `pdm add -d` do?
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
embed-repo-link "We've added a new \`[dev-dependencies]\` sub-table to the \`[tool.pdm]\` table of {pyproject.toml}, which contains \`black\`:"
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
simple-diff --context 2 HEAD~ pyproject.toml | show-code toml
```

<!-- #region slideshow={"slide_type": "notes"} -->
When we run `pdm install`, by default, PDM will install dependencies from here in addition to the dependencies listed in `[project.dependencies]`.  A different tool like `pip`, however, will not.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on adding development dependencies](https://pdm.fming.dev/latest/usage/dependency/#add-development-only-dependencies) for more information on development dependencies.
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

We can now run `black` within our environment.
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# This cell hidden in presentation and docs
cat << "EOF" > src/eeskew_pwg_test_000/sarcasm.py
import cowsay
def sarcasm(
            s
          ):
    """Convert string `s` to sArCaSm TeXt."""
    out = ''
    for i,c in \
        enumerate( s ):

        if i% 2 ==0: out +=c.lower()

        else:



            out+= c.upper()

    return out

def sarcastic_cowsay(s):
    """Cowsay `s`, sArCaStIcAlLy."""
    sarcastic_s = sarcasm(s); cowsay.cow(sarcastic_s)
EOF
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git-checkpoint
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
embed-repo-link "Let's re-write {src/eeskew_pwg_test_000/sarcasm.py} with deliberately poor formatting:"
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
simple-diff HEAD~ src/eeskew_pwg_test_000/sarcasm.py | show-code python
```

<!-- #region slideshow={"slide_type": "subslide"} -->
This is bad formatting!  Rather than fix it manually, we can run `black` on our code, which will auto-impose a reasonable style.
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run black src/
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git-checkpoint
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What did `black` do?
<!-- #endregion -->

```bash slideshow={"slide_type": "notes"} trusted=true tags=["remove-input"]
embed-repo-link "\`black\` has automatically re-formatted {src/eeskew_pwg_test_000/sarcasm.py}, fixing the poor formatting we introduced earlier:"
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
simple-diff HEAD~ src/eeskew_pwg_test_000/sarcasm.py | show-code python
```

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

In [Part 2](part2.ipynb), we'll cover how to publish a PDM project on PyPI, so that it can be installed with a simple `pip install`.
<!-- #endregion -->
