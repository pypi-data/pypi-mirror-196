# My python package

## Get started

## Pre-requisites

Install necessary dependencies for developement

```shell
pip install twine build setuptools
```

## Develop

1. Clone project and reset git history

```shell
git clone https://github.com/ablil/python-starter pypkg && cd pypkg && rm -rf .git && git init && git add . && git commit -m 'initial commit'
```

2. Run your tests

```shell

```

## Build and publish

* Build

```shell
rm -rf dist && python -m build
```

* Publish to TestPyPi

```shell
python -m twine upload --repository testpypi dist/*
```

* Publish to PyPi

```shell
python -m twine upload --repository testpypi dist/*
```