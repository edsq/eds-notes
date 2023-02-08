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
# Python project management, packaging, and publishing on PyPI

Presentation for the WSU Python Working Group
February 8, 2023

Edward Eskew
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
# Overview

1. Beyond the standard library with `pip`
2. Virtual environments
3. Using `conda` for environment and dependency management
4. Using `pdm` for project management
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
# The standard library

- Comes with every installation of python
- Very capable!
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
from random import gauss
from statistics import stdev

data = [gauss(sigma=10.0) for _ in range(1000)]
sigma = stdev(data)
print(sigma)
```

<!-- #region slideshow={"slide_type": "fragment"} -->
- Of course, many of the most useful tools in python come from outside the standard library
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
import matplotlib.pyplot as plt

plt.hist(data, bins=100)
```
