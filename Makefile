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

clean:
	rm -rf notebooks
	rm -rf .venv

.PHONY: init clean notebook-server
