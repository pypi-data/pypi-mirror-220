# Contributing

## Setting up local development

Clone the Git repository:

```console
git clone https://github.com/kianmeng/txt2ebook
cd txt2ebook
```

To set up different Python environments, we need to install all supported
Python version using <https://github.com/pyenv/pyenv>. Once you've installed
Pyenv, install these additional Pyenv plugins:

```console
git clone https://github.com/pyenv/pyenv-doctor.git "$(pyenv root)/plugins/pyenv-doctor"
pyenv doctor

git clone https://github.com/pyenv/pyenv-update.git $(pyenv root)/plugins/pyenv-update
pyenv update
```

Run the command below to install all Python versions:

```console
pyenv install $(cat .python-version)
```

Setting up development environment and install dependencies:

```console
python -m pip install --upgrade pip poetry
poetry install
poetry check
poetry config virtualenvs.prefer-active-python true
```

Spawn a shell in virtual environment for your development:

```console
poetry shell
```

Show all available tox tasks:

```console
$ tox -av
...
default environments:
py38  -> testing against python3.8
py39  -> testing against python3.9
py310 -> testing against python3.10
py311 -> testing against python3.11

additional environments:
cov   -> generate code coverage report in html
doc   -> generate sphinx documentation in html
pot   -> update translations (pot/po/mo) files
```

To run specific test:

```console
tox -e py37,py38,py39,py310,py311 -- tests/test_tokenizer.py
```

For code lint, we're using `pre-commit`:

```console
pre-commit install # run once
pre-commit clean
pre-commit run --all-files
```

Or specific hook:

```console
pre-commit run pylint -a
```

We're using zero-based versioning.

For patches or bug fixes:

```console
poetry version patch
```

For feature release:

```console
poetry version minor
```

## Create a Pull Request

Fork it at GitHub, <https://github.com/kianmeng/txt2ebook/fork>

Create your feature branch:

```console
git checkout -b my-new-feature
```

Commit your changes:

```console
git commit -am 'Add some feature'
```

Push to the branch:

```console
git push origin my-new-feature
```

Create new Pull Request in GitHub.

## License

By contributing to `txt2ebook`, you agree that your contributions will be
licensed under the [LICENSE.md](./LICENSE.md) file in the root directory of
this source tree.
