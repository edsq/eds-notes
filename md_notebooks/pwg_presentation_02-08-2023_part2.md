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
# Publishing on (Test)PyPI

Part 2 of notes from a talk given to the WSU Python Working Group on February 8, 2023.

Here, we'll cover the basics of publishing a project on PyPI or TestPyPI using PDM,
including managing relevant project metadata.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{note}
A companion repository with the example project created in these notes is available [here](https://github.com/edsq/eeskew-pwg-test-000).
:::
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# Make sure we're in the repo directory
# Note: if cwd is already the companion repo, this will fail.
# Either restart the kernel first or don't run this cell, in that case.
project_dir=$(pdm info --where)
cd $project_dir/repos/eeskew-pwg-test-000
```

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# Start at the last checkpoint from Part 1
git add -A
git checkout 6ed1de5
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Package version

Right now, the package version (`"0.1.0"`) is stored in the `pyproject.toml` file (in the `project.version` keyword).  The best practice is to place this in a `__version__.py` file, and have that be the single source of truth for our package version.

Create a `__version__.py` file in `src/eeskew_pwg_test_000`, and add the `__version__` variable to it.  The new file should look like:
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# This cell hidden in presentation and docs
echo '__version__ = "0.1.0"' > src/eeskew_pwg_test_000/__version__.py
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
FILE="src/eeskew_pwg_test_000/__version__.py"

echo "\`\`\`python
# $FILE
$(cat $FILE)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Now modify the `pyproject.toml` file so that the version is [dynamic metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#dynamic):
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

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

<!-- #region slideshow={"slide_type": "fragment"} -->
Note the new `project.dynamic` array, the new `tool.pdm.version` table, and that the `project.version` key is gone.

We can check the version like so:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm show --version eeskew-pwg-test-000
```

<!-- #region slideshow={"slide_type": "subslide"} -->
We should also add the `__version__` variable to our `__init__.py`:
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# This cell hidden in presentation and docs
echo 'from eeskew_pwg_test_000.__version__ import __version__' > src/eeskew_pwg_test_000/__init__.py
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
echo "\`\`\`python
$(simple-diff HEAD~ src/eeskew_pwg_test_000/__init__.py)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "fragment"} -->
This allows us to check the version from python in the conventional way:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run python -c "import eeskew_pwg_test_000; print(eeskew_pwg_test_000.__version__)"
```

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on dynamic versioning](https://pdm.fming.dev/latest/pyproject/build/#dynamic-versioning) for more information.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Packaging the project

Let's review the project as it exists so far:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
tree
```

<!-- #region slideshow={"slide_type": "subslide"} -->
To create an [sdist](https://packaging.python.org/en/latest/specifications/source-distribution-format/) and [wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/):
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm build
```

<!-- #region slideshow={"slide_type": "slide"} -->
### What happened?

We've created a new directory named `dist`, where these two distribution formats have been placed.
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
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

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on publishing to PyPI for more information](https://pdm.fming.dev/latest/usage/project/#publish-the-project-to-pypi).
:::
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# This cell hidden in presentation and docs
cat << "EOF" > pyproject.toml
[tool.pdm]
version = { source = "file", path = "src/eeskew_pwg_test_000/__version__.py" }

[tool.pdm.scripts]
test-publish.shell = '''\
VERSION=$(pdm show --version eeskew-pwg-test-000)
pdm bump patch > /dev/null
BUMPED_VERSION=$(pdm show --version eeskew-pwg-test-000)
DEV_VERSION=$BUMPED_VERSION.dev$(date +%s)
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash tags=["remove-input"] slideshow={"slide_type": "subslide"} trusted=true
echo "\`\`\`toml
$(simple-diff HEAD~ pyproject.toml)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "skip"} -->
Click below to show diff:
<!-- #endregion -->

```bash tags=["remove-input", "hide-output"] slideshow={"slide_type": "notes"} trusted=true
git diff --color HEAD~ pyproject.toml | ../../scripts/diff-so-fancy
```

<!-- #region slideshow={"slide_type": "subslide"} -->
When we run `pdm run test-publish`, this script:
1. Gets the current version with `pdm show --version`
2. Changes the package version to a patch bump of that version with `.dev{date in seconds}` appended.  This is a [developmental release](https://peps.python.org/pep-0440/#developmental-releases) format.
3. Publishes the package on TestPyPI
4. Returns the package version to its original value

Let's run it!
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run test-publish
```

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PDM docs on PDM scripts](https://pdm.fming.dev/latest/usage/scripts/) for more information on writing PDM scripts.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Other project metadata

There is quite a bit of project metadata we can specify in `pyproject.toml` - here are some other examples.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{seealso}
See the [PyPA specification](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/) for a complete list of possible metadata keys.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Add an entry point to the package
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "notes"} -->
If we're developing a command-line application, we want our users to be able to run the application with a single command, not something like `python path_to_script/script.py`.  We can enable this by adding an [entry point](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#entry-points) to `pyproject.toml`.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
First, add a new module and new function:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} trusted=true tags=["remove-input"]
echo "\`\`\`python
$(simple-diff HEAD~ src/eeskew_pwg_test_000/cli.py)
\`\`\`" | displayMD
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Now let's add the script to `pyproject.toml`:
<!-- #endregion -->

```bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# This cell hidden in presentation and docs
cat << "EOF" > pyproject.toml
[tool.pdm]
version = { source = "file", path = "src/eeskew_pwg_test_000/__version__.py" }

[tool.pdm.scripts]
test-publish.shell = '''\
VERSION=$(pdm show --version eeskew-pwg-test-000)
pdm bump patch > /dev/null
BUMPED_VERSION=$(pdm show --version eeskew-pwg-test-000)
DEV_VERSION=$BUMPED_VERSION.dev$(date +%s)
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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

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

<!-- #region slideshow={"slide_type": "fragment"} -->
Note the new entry for `sarcasticow` in the `project.scripts` table.

To use the `sarcasticow` command, we need to re-install the project:
<!-- #endregion -->

```bash slideshow={"slide_type": "subslide"} trusted=true
pdm install
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Now we can run our command from within the environment:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run sarcasticow "I'm a sarcastic cow"
```

<!-- #region slideshow={"slide_type": "notes"} -->
:::{note}
Because we're using `pdm` for environment management, we still need to use `pdm run` to access the script installed into the virtual environment.

Unlike the `test-publish` PDM script we wrote earlier, if we activated the environment with `source .venv/bin/activate`, we could simply use the `sarcasticow` command by itself, and users who install our package with `pip` into their own virtualenv or conda environment will also have access to `sarcasticow`.  Even better, users who install our package through [`pipx`](https://pypa.github.io/pipx/) will be able to use the `sarcasticow` command without activating a virtual environment.
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Updating README

Thus far, we've left our README as an empty file.  This is bad.  Let's update it to show our utility's usage:
<!-- #endregion -->

````bash tags=["remove-cell"] slideshow={"slide_type": "skip"} trusted=true
# This cell hidden in presentation and docs
cat << "EOF" > README.md
# eeskew-pwg-test-000

This is a companion repository to the presentation [Project Management and Publishing with PDM](https://edsq.github.io/eds-notes/pwg_presentation_02-08-2023.html).

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

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

```bash slideshow={"slide_type": "fragment"} tags=["remove-input"] trusted=true
simple-diff HEAD~ README.md
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Project URLs

We can add relevant URLs in the [`urls` table](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#urls), which will appear in the sidebar on PyPI.

Here, we set `Documentation` to a link to our docs (this Jupyter Book), and `Repository` to the GitHub repo for this code.
<!-- #endregion -->

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# This cell hidden in presentation and docs
cat << "EOF" > pyproject.toml
[tool.pdm]
version = { source = "file", path = "src/eeskew_pwg_test_000/__version__.py" }

[tool.pdm.scripts]
test-publish.shell = '''\
VERSION=$(pdm show --version eeskew-pwg-test-000)
pdm bump patch > /dev/null
BUMPED_VERSION=$(pdm show --version eeskew-pwg-test-000)
DEV_VERSION=$BUMPED_VERSION.dev$(date +%s)
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

[project.urls]
Documentation = "https://edsq.github.io/eds-notes/pwg_presentation_02-08-2023.html"
Repository = "https://github.com/edsq/eeskew-pwg-test-000"

[project.scripts]
sarcasticow = "eeskew_pwg_test_000.cli:main"

[build-system]
requires = ["pdm-pep517>=1.0"]
build-backend = "pdm.pep517.api"
EOF
```

```bash slideshow={"slide_type": "skip"} tags=["remove-cell"] trusted=true
# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit
```

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

<!-- #region slideshow={"slide_type": "subslide"} -->
Finally, we publish again to TestPYPI:
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"} trusted=true
pdm run test-publish
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Our page on TestPyPI now shows the README, and the documentation and repository links are available on the sidebar:
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "skip"} -->
:::{image} images/testpypi_project_screenshot.png
:::
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Conclusion

And that's it!  We've gone through the basics of project management, packaging, and publishing on (Test)PyPI.

### Further reading

Some good articles for further reading:

- The official [PyPA packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) is a good place to start.
- I have taken quite a bit of inspiration in my work from the great series [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) by Claudio Jolowicz.  It goes into much greater detail on various points of project management than I did here, and is well worth a read.
    - Hypermodern Python uses the project manager [Poetry](https://python-poetry.org), not PDM (see my thoughts on that below), but PDM can do nearly everything Poetry can do, so this series is still useful.
- [How to improve Python packaging, or why fourteen tools are at least twelve too many](https://chriswarrick.com/blog/2023/01/15/how-to-improve-python-packaging/) is a good overview of the mess of modern python project management tools.

Some important accepted Python Enhancement Proposals that shape the modern python packaging ecosystem:

- [PEP 621](https://peps.python.org/pep-0621/) (project metadata in `pyproject.toml`)
- [PEP 508](https://peps.python.org/pep-0508/) (dependency specification syntax)
- [PEP 440](https://peps.python.org/pep-0440/) (version numbers for dependency specification)
- [PEP 517](https://peps.python.org/pep-0517/) (specifying the build backend in `pyproject.toml` independently of the build frontend)


### Other project management tools

You'll note that Hypermodern Python recommends using the project manager [Poetry](https://python-poetry.org).  Poetry was a cutting-edge option at the time that series was written, and it has grown to considerable popularity.  I chose not to recommend it in this tutorial for several reasons:

- Poetry is not fully [PEP 517](https://peps.python.org/pep-0517/) compliant.  This means you and your users will not be able to use any other tool to build and install your project.
- By default, Poetry imposes an upper bound on dependency version numbers.  This goes against [Python standards](https://peps.python.org/pep-0440/) and will likely cause problems down the line: see articles [here](https://iscinumpy.dev/post/bound-version-constraints/) and [here](https://iscinumpy.dev/post/poetry-versions/).
- The Poetry developers chose to "deprecate" their old install script by [*causing it to randomly fail*](https://youtu.be/Gr9o8MW_pb0?t=290) instead of sunsetting with a typical deprecation warning.  This bizarre choice raises serious concerns about the future of the application.
- PDM has considerably fewer open issues on GitHub than Poetry: at the time of this writing, [34](https://github.com/pdm-project/pdm/issues) vs [575](https://github.com/python-poetry/poetry/issues).
    - Some of this is explainable by PDM having fewer users than Poetry.  However, PDM has 4.1k stars on Github vs. Poetry's 24.1k, so using those stars as a proxy for the number of users, we see Poetry has 17 times the number of open issues but only 6 times the number of users as PDM.
- The Poetry developers are famously stubborn and slow to implement new python standards, while the PDM developer is remarkably responsive and active in development.
- Poetry is much more inflexible about resolving dependency conflicts than PDM, which quickly becomes a huge headache for complicated projects.

Another project manager worth looking in to is [Hatch](https://hatch.pypa.io/latest/).  I don't have any experience with this particular tool, but it does support modern Python standards and has the benefit of being an official part of the Python Packaging Authority (PyPA).  However, it does not have lockfile support, as there is not yet an established standard (PEP [665](https://peps.python.org/pep-0665/) was an attempt, but it was rejected).  If you don't need a lockfile in your work, it may be worth considering.

Finally, for those using `conda`, [anaconda-project](https://anaconda-project.readthedocs.io/en/latest/) deserves a mention.  It isn't a full-fledged project manager (for example, you can't easily use it to publish on PyPI), but it does dramatically simplify sharing and running code.
<!-- #endregion -->