# Project management, packaging, and publishing on PyPI

Presentation given to the WSU Python Working Group on February 8, 2023.

## Installing

1. Install the package:
```
pdm install
```

2. Generate the notebooks from synced markdown files using `jupytext`:
```
pdm run jupytext --sync md_notebooks/*
```

3. (If you intend to commit to the repository) Install pre-commit hooks:
```
pdm run pre-commit install
```
