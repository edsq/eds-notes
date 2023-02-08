
PROJECT_DIR ?= "tst"

all:
	@make $(PROJECT_DIR)/mypyproject.toml

init:
	pdm install
	pdm run python -m bash_kernel.install
	pdm run jupytext --sync md_notebooks/*
	# Test for git https://stackoverflow.com/a/57340232/1088938
	-git tag > /dev/null 2>&1 && pdm run pre-commit install

notebook-server: .venv
	pdm run jupyter notebook

.venv:
	@make init

$(PROJECT_DIR):
	mkdir -p $@

$(PROJECT_DIR)/pyproject.toml: resources/skeleton/pyproject.toml $(PROJECT_DIR) 
	sed 's/VAR/REP/g' $< > $@

clean:
	rm -rf notebooks
	rm -rf .venv
	rm -f .pdm.toml

.PHONY: all init clean notebook-server
