# myco-ai

[![Validation Workflow](https://github.com/mbeacom/myco-ai/actions/workflows/validate.yaml/badge.svg?branch=main&event=push)](https://github.com/mbeacom/myco-ai/actions/workflows/validate.yaml)
[![Pre-Commit Checks Workflow](https://github.com/mbeacom/myco-ai/actions/workflows/pre-commit.yaml/badge.svg?branch=main&event=push)](https://github.com/mbeacom/myco-ai/actions/workflows/pre-commit.yaml)
[![Coverage Status](https://codecov.io/github/mbeacom/myco-ai/coverage.svg?branch=main)](https://codecov.io/github/mbeacom/myco-ai?branch=main)
[![PyPi](https://img.shields.io/pypi/v/myco-ai-x)](https://pypi.org/project/myco-ai-x/)

This project is meant to be an assistant for mycologists.

## Usage

This project uses:

- [poetry](https://python-poetry.org/) for dependency management and packaging.
- [poethepoet](https://poethepoet.natn.io/) for task running.
- [pytest](https://docs.pytest.org/en/stable/) for testing.
- [black](https://black.readthedocs.io/en/stable/) for auto-formatting.
- [mypy](https://mypy.readthedocs.io/en/stable/) for static type checking.
- [pre-commit](https://pre-commit.com/) for git hooks.
- [ruff](https://beta.ruff.rs/docs/) for linting.
- [mkdocs](https://www.mkdocs.org/) for documentation.

Ensure you have installed the relevant dependencies before continuing.

### Install dependencies

```bash
poetry install
```

### Run tests

```bash
poetry poe test
# or: poetry run poe test
```
