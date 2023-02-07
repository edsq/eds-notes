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

# Creating a PDM project

Creating an example PDM project.  Unfortunately, the interactive `pdm init` command does not work in a Jupyter notebook (and the defaults it chooses in non-interactive mode are not good), so we have to do this by hand.  Note that we have to `cd` into the project directory in every new bash cell because the CWD is reset between them.

```bash
mkdir test_pdm_project
cd test_pdm_project
touch README.md  # Create an empty README file
```

```bash
cd test_pdm_project

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

```bash
cd test_pdm_project

# Get the current working directory
CWD=$(pwd)

# Create the .pdm.toml file
cat << EOF > .pdm.toml
[venv]
in_project = true

[python]
path = "$CWD/.venv/bin/python"
EOF
```

```bash
cd test_pdm_project
pdm install
```

## Deleting test project

```bash
rm -r test_pdm_project
```

```python

```
