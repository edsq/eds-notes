#!/usr/bin/env python
# coding: utf-8

# # Project Management and Publishing with PDM
# 
# Requirements:
# 
# - The ability to get python executables of different versions, such as with [pyenv](https://github.com/pyenv/pyenv) or [conda](https://docs.conda.io/en/latest/miniconda.html)
# - [PDM](https://pdm.fming.dev/latest/) available globally

# First, create the project directory and `cd` into it:
# 
# ```bash
# mkdir eeskew-pwg-test-000
# cd eeskew-pwg-test-000
# ```
# 
# Note - because this is a throwaway test project, it is important that you give your project a name that won't conflict with any other package on PyPI or TestPyPI.  Adding your name and some numbers is a good way to ensure this.

# ## Set the python version and initialize the project
# 
# Here, we'll use python version 3.11, but you may change this to be whatever you like.
# 
# ### Using `pyenv` (recommended)
# 
# Install python 3.11 if it is not already (see installed versions with `pyenv versions`):
# 
# ```bash
# pyenv install 3.11
# ```
# 
# Set the local python version for this project and initialize using that version:
# 
# ```bash
# pyenv local 3.11
# pdm init --python python
# ```

# `pyenv local` creates a file `.python-version` which `pyenv` uses to redirect the command `python` to the `python3.11`.  Thus, we only need to tell pdm to use the usual `python` executable.

# ### Using `conda`
# 
# Here, we'll use `conda` to get a particular python version, but we won't activate the conda environment (except to get a path to the `python` executable).  Environment management will be handled by PDM.
# 
# Get python 3.11:
# 
# ```bash
# conda create -y -p .conda_env python=3.11
# pdm init --python .conda_env/bin/python
# ```

# ### Documentation implementation
# 
# The following commands will be equivalent to the above, but work when run from inside the documentation.

# In[1]:


get_ipython().run_cell_magic('bash', '', 'cd ..\nrm -r eeskew-pwg-test-000  # remove the test project if it already exists\nmkdir eeskew-pwg-test-000\ncd eeskew-pwg-test-000\ncp -a ../resources/skeleton/ .\npdm venv create python\n')


# In[2]:


# Change directory in python so that the python kernel remembers
import os
os.chdir(os.path.join('..', 'eeskew-pwg-test-000'))


# In[3]:


get_ipython().run_cell_magic('bash', '', 'pdm info\n')


# ## The PDM project
# 
# Let's take a look at what we've created:

# In[4]:


get_ipython().run_cell_magic('bash', '', 'ls -a\n')


# ## The `pyproject.toml` file

# In[5]:


get_ipython().run_cell_magic('bash', '', 'cat pyproject.toml\n')


# ## Adding code

# In[6]:


get_ipython().run_cell_magic('bash', '', 'mkdir src\nmkdir src/eeskew_pwg_test_000\ntouch src/eeskew_pwg_test_000/__init__.py\n')


# ### Add a module
# 
# Let's add some code in `src/eeskew_pwg_test_000/utils.py`:

# In[7]:


get_ipython().run_cell_magic('writefile', 'src/eeskew_pwg_test_000/utils.py', '\ndef sarcasm(s):\n    """Convert string `s` to sArCaSm TeXt."""\n    out = \'\'\n    for i, c in enumerate(s):\n        if i % 2 == 0:\n            out += c.lower()\n        else:\n            out += c.upper()\n    return out\n')


# ## Install the project

# In[8]:


get_ipython().run_cell_magic('bash', '', 'pdm install\n')


# Now we can import our package:

# In[9]:


get_ipython().run_cell_magic('bash', '', 'pdm run python -c "from eeskew_pwg_test_000.utils import sarcasm; print(sarcasm(\'Hello world!\'))"\n')


# Note we have to type `pdm run` before our command for it to be run within our project environment.

# ## Add a dependency
# 
# Let's add a dependency to our project:

# In[10]:


get_ipython().run_cell_magic('bash', '', '\npdm add cowsay\n')


# ### What did `pdm add` do?
# 
# `cowsay` now appears as a dependency in `pyproject.toml`:

# In[11]:


get_ipython().run_cell_magic('bash', '', 'cat pyproject.toml\n')


# We can now also import `cowsay`:

# In[12]:


get_ipython().run_cell_magic('bash', '', 'pdm run python -c "import cowsay; cowsay.cow(\'moo!\')"\n')


# ## Adding more code
# 
# Let's add a new function to `utils.py`:

# In[13]:


get_ipython().run_cell_magic('writefile', 'src/eeskew_pwg_test_000/utils.py', 'import cowsay\n\ndef sarcasm(s):\n    """Convert string `s` to sArCaSm TeXt."""\n    out = ""\n    for i, c in enumerate(s):\n        if i % 2 == 0:\n            out += c.lower()\n\n        else:\n            out += c.upper()\n\n    return out\n\ndef sarcastic_cowsay(s):\n    """Cowsay `s`, sArCaStIcAlLy."""\n    sarcastic_s = sarcasm(s)\n    cowsay.cow(sarcastic_s)\n')


# We can now run this new function:

# In[14]:


get_ipython().run_cell_magic('bash', '', 'pdm run python -c "from eeskew_pwg_test_000.utils import sarcastic_cowsay; sarcastic_cowsay(\'mooo!\')"\n')


# ## Add a development dependency
# 
# The dependencies listed in the `project.dependencies` section of `pyproject.toml` will all be installed when someone runs `pip install eeskew_pwg_test_project`.  What if we have dependencies we only want in our development environment?
# 
# Let's add `black`, a tool to automatically format our code:

# In[15]:


get_ipython().run_cell_magic('bash', '', 'pdm add -d black\n')


# ### What happened?

# In[16]:


get_ipython().run_cell_magic('bash', '', 'cat pyproject.toml\n')


# ## Using black
# 
# We can now run `black` within our environment.  Let's re-write our code with poor formatting (note the spacing around the `==`, `%`, and `+=` operators), and then run `black` on it:

# In[17]:


get_ipython().run_cell_magic('writefile', 'src/eeskew_pwg_test_000/utils.py', 'import cowsay\n\ndef sarcasm(s):\n    """Convert string `s` to sArCaSm TeXt."""\n    out = \'\'\n    for i,c in enumerate(s):\n        if i% 2 ==0:\n            out +=c.lower()\n\n        else:\n            out+= c.upper()\n\n    return out\n\ndef sarcastic_cowsay(s):\n    """Cowsay `s`, sArCaStIcAlLy."""\n    sarcastic_s = sarcasm(s)\n    cowsay.cow(sarcastic_s)\n')


# In[18]:


get_ipython().run_cell_magic('bash', '', 'pdm run black src/\n')


# ### What happened?

# In[19]:


get_ipython().run_cell_magic('bash', '', 'cat src/eeskew_pwg_test_000/utils.py\n')


# ## Packaging the project
# 
# Let's review the project as it exists so far:

# In[20]:


get_ipython().run_cell_magic('bash', '', 'tree\n')


# To create a [sdist](https://packaging.python.org/en/latest/specifications/source-distribution-format/) and [wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/):

# In[21]:


get_ipython().run_cell_magic('bash', '', 'pdm build\n')


# ### What happened?
# 
# We've created a new directory named `dist`, where these two distribution formats have been placed.

# In[22]:


get_ipython().run_cell_magic('bash', '', 'tree\n')


# We could install this project into a different python environment with `python -m pip install dist/eeskew-pwg-test-000-0.1.0.tar.gz` or `python -m pip install dist/eeskew_pwg_test_000-0.1.0-py3-none-any.whl` (the latter is faster).

# ## Publishing the project
# 
# Now we'll publish the project on (Test)PyPI.
# 
# 0. First, make an account on [TestPyPI](https://test.pypi.org).

# 1. Navigate to your account settings, scroll down to "API tokens", and click "Add API token"

# 2. Give the token a descriptive name, set the scope to "Entire account (all projects)", and click "Add token".

# 3. Copy the token that appears - heeding the warning that it will appear only once!

# 4. Now we'll configure PDM with these credentials (replacing `<PASTE_YOUR_TOKEN_HERE>` with the token you've just copied:
# 
# ```bash
# pdm config repository.testpypi.username "__token__"
# pdm config repository.testpypi.password "<PASTE_YOUR_TOKEN_HERE>"
# ```

# 5. Finally, to publish on TestPyPI, just run
# 
# ```bash
# pdm publish -r testpypi
# ```
# 
# Note that you do not need to run `pdm build` first - PDM will build the distribution as part of `publish` anyway.

# ## Updating your project
# 
# Let's add an entrypoint for our project in `pyproject.toml`.  First, add a new module and new function:

# In[23]:


get_ipython().run_cell_magic('writefile', 'src/eeskew_pwg_test_000/cli.py', 'import argparse\n\nfrom eeskew_pwg_test_000.utils import sarcastic_cowsay\n\ndef main():\n    """Cowsay something sarcastically from the command line."""\n    parser = argparse.ArgumentParser()\n    parser.add_argument("speech")\n    args = parser.parse_args()\n    \n    s = args.speech\n    sarcastic_cowsay(s)\n')


# Now let's add the script to `pyproject.toml`:

# In[24]:


get_ipython().run_cell_magic('writefile', 'pyproject.toml', '[tool.pdm]\n[tool.pdm.dev-dependencies]\ndev = [\n    "black>=23.1.0",\n]\n\n[project]\nname = "eeskew-pwg-test-000"\nversion = "0.1.0"\ndescription = "A test project for presentation to the WSU Python Working Group."\nauthors = [\n    {name = "Edward Eskew", email = "edward.eskew@wsu.edu"},\n]\ndependencies = [\n    "cowsay>=5.0",\n]\nrequires-python = ">=3.11"\nreadme = "README.md"\nlicense = {text = "MIT"}\n\n[project.scripts]\nsarcasticow = "eeskew_pwg_test_000.cli:main"\n\n[build-system]\nrequires = ["pdm-pep517>=1.0"]\nbuild-backend = "pdm.pep517.api"\n')


# In[25]:


get_ipython().run_cell_magic('bash', '', 'pdm install\n')


# Now we can run our command from within the environment:

# In[26]:


get_ipython().run_cell_magic('bash', '', 'pdm run sarcasticow "I\'m a sarcastic cow"\n')


# ## Updating README
# 
# Let's update our README to show this usage:

# In[27]:


get_ipython().run_cell_magic('writefile', 'README.md', '# eeskew-pwg-test-000\n\nCommand-line usage:\n\n```\n$ sarcasticow "I\'m a sarcastic cow"\n\n  ___________________\n| i\'m a sArCaStIc cOw |\n  ===================\n                   \\\n                    \\\n                      ^__^\n                      (oo)\\_______\n                      (__)\\       )\\/\\\n                          ||----w |\n                          ||     ||\n\n```\n')


# Now we can bump the version and publish again to TestPyPI:

# In[28]:


get_ipython().run_cell_magic('writefile', 'pyproject.toml', '[tool.pdm]\n[tool.pdm.dev-dependencies]\ndev = [\n    "black>=23.1.0",\n]\n\n[project]\nname = "eeskew-pwg-test-000"\nversion = "0.2.0"\ndescription = "A test project for presentation to the WSU Python Working Group."\nauthors = [\n    {name = "Edward Eskew", email = "edward.eskew@wsu.edu"},\n]\ndependencies = [\n    "cowsay>=5.0",\n]\nrequires-python = ">=3.11"\nreadme = "README.md"\nlicense = {text = "MIT"}\n\n[project.scripts]\nsarcasticow = "eeskew_pwg_test_000.cli:main"\n\n[build-system]\nrequires = ["pdm-pep517>=1.0"]\nbuild-backend = "pdm.pep517.api"\n')


# ```bash
# pdm publish -r testpypi
# ```

# ## Conclusion
# 
# And that's it!  We've gone through the basics of project management, packaging, and publishing on (Test)PyPI.  Any questions?
