# Working notes

## Outline of PWG 02-08-2023 presentation
I didn't get to most of this, as the presentation was long enough already.  I'm keeping
it as a record of topics I'd like to eventually cover.

- Overview
- Maybe: python imports
  - standard library vs external packages
  - python path
- Explaining pip 
  - maybe: where pip installs by default in python path
  - Explaining PyPI
  - Why using pip in base environment is bad
- Explaining virtual environments
  - maybe: mechanics of activating a virtual environment (path, etc)
  - why virtual environments come up short
    - pip's dependency resolution is bad
    - reproducibility is bad
    - no packaging & publishing
- An alternative: conda
  - why not conda
    - slow dependency resolution
    - no lockfile
    - no packaging & publishing
- Maybe: new PEP standards
  - [621](https://peps.python.org/pep-0621/) (project metadata in `pyproject.toml`)
  - [508](https://peps.python.org/pep-0508/) (dependency specification syntax)
  - [440](https://peps.python.org/pep-0440/) (version numbers for dependency specification)
  - [517](https://peps.python.org/pep-0517/) (specifying the build backend in `pyproject.toml` independently of the build frontend)
- pdm
  - maybe: install pdm with pipx
  - create project
  - install dependencies
  - install dev dependencies
  - publish
