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

```bash slideshow={"slide_type": "skip"}
bind "set show-mode-in-prompt off"  # Turn off showing the vi mode in prompt, which clutters up the output here
```

<!-- #region slideshow={"slide_type": "slide"} -->
# Creating a PDM project

Creating an example PDM project.  Unfortunately, the interactive `pdm init` command does not work in a Jupyter notebook (and the defaults it chooses in non-interactive mode are not good), so we have to do this by hand.
<!-- #endregion -->

```bash slideshow={"slide_type": "slide"}
mkdir test_pdm_project
cd test_pdm_project
touch README.md  # Create an empty README file
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Creating the `pyproject.toml` file

This file would typically be created automatically by the `pdm init` command.
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
# Create the pyproject.toml file
cat << EOF > pyproject.toml
[project]
name = "test_pdm_project"
version = "0.1.0"
description = ""
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
EOF
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Creating the `.pdm.toml` file

This file would also be automatically created by the `pdm init` command.
<!-- #endregion -->

```bash slideshow={"slide_type": "fragment"}
# Get the current working directory
CWD=$(pwd)

# Create the .pdm.toml file
cat << EOF > .pdm.toml
[venv]
in_project = true  # Ensures PDM doesn't try to use the venv this notebook is running in

[python]
path = "$CWD/.venv/bin/python"
EOF
```

```bash slideshow={"slide_type": "slide"}
# Create a virtual environment in the directory ./.venv
python -m venv .venv
```

```bash slideshow={"slide_type": "slide"}
pdm install
```

```bash slideshow={"slide_type": "slide"}
pdm info
```

```bash

```
