bind "set show-mode-in-prompt off"  # Turn off showing the vi mode in prompt, which clutters up the output here

# This cell hidden in presentation and docs
cd ../eeskew-pwg-test-000
git clean -dfx  # remove all untracked files (src, build, dist, .venv)
git checkout $(git rev-list --topo-order main | tail -1)  # check out first commit
pdm venv create --force python

# This cell hidden in presentation and docs
# Check that the environment and project are correct
pdm info

ls -a

cat pyproject.toml

mkdir src
mkdir src/eeskew_pwg_test_000
touch src/eeskew_pwg_test_000/__init__.py

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

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

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

cat src/eeskew_pwg_test_000/utils.py

pdm install

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

pdm run python -c 'from eeskew_pwg_test_000.utils import sarcasm; print(sarcasm("Hello world!"))'

ls

cat pdm.lock

pdm add cowsay

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy

cat pdm.lock

pdm run python -c 'import cowsay; cowsay.cow("moo!")'

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

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ src/eeskew_pwg_test_000/utils.py | ../scripts/diff-so-fancy

pdm run python -c 'from eeskew_pwg_test_000.utils import sarcastic_cowsay; sarcastic_cowsay("mooo!")'

pdm add -d black

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy

cat pdm.lock

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

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ src/eeskew_pwg_test_000/utils.py | ../scripts/diff-so-fancy

pdm run black src/

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ src/eeskew_pwg_test_000/utils.py | ../scripts/diff-so-fancy

# This cell hidden in presentation and docs
echo '__version__ = "0.1.0"' > src/eeskew_pwg_test_000/__version__.py

cat src/eeskew_pwg_test_000/__version__.py

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

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy

pdm show --version

# This cell hidden in presentation and docs
echo 'from eeskew_pwg_test_000.__version__ import __version__' > src/eeskew_pwg_test_000/__init__.py

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ src/eeskew_pwg_test_000/__init__.py | ../scripts/diff-so-fancy

pdm run python -c "import eeskew_pwg_test_000; print(eeskew_pwg_test_000.__version__)"

tree

pdm build

tree

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

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy

pdm run test-publish

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

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

cat src/eeskew_pwg_test_000/cli.py

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

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ pyproject.toml | ../scripts/diff-so-fancy

pdm install

pdm run sarcasticow "I'm a sarcastic cow"

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

# checkpoint
git add -A
git checkout $(git rev-list --topo-order HEAD...main | tail -1)  # check out next commit

git diff HEAD~ README.md | ../scripts/diff-so-fancy

pdm run test-publish
