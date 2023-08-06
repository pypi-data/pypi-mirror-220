## PyUtils
The PyUtils package is intended to be a collection of utility functions for Python engineers. It aims to provide reusable code snippets that simplify common tasks in Python programming.

## Features
- String Manipulation
- File Handling
- Data Conversion
- Date/Time Operations

## Tech Stacks
- Python

## Local Environment

Setup virtual environment and Poetry:
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry config virtualenvs.create false
```
Install project packages:
```shell
poetry install
```
Run tests:
```shell
pytest
```
Run tests coverage:
```shell
pytest --cov=pyutils tests/
```

## Documentation
Show Docs Locally:
  ```shell
  mkdocs serve
  ```
Deploy Docs to GitHub Pages:
  ```shell
  mkdocs gh-deploy
  ```

## Build
Build the project:
```shell
python3 -m build
```

## Distribution
Distribute the package to PyPI
```shell
python3 -m twine upload --repository pypi dist/*
```
