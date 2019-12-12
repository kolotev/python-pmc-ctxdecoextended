# python-pmc-ctxdecoextended

## Install

Regular use _(assuming that you've already published your package on NCBI Artifactory PyPI)_:

```sh
pip install pmc-ctxdecoextended  # or add it to your requirements file
```

For development:

```sh
git clone ssh://git@bitbucket.be-md.ncbi.nlm.nih.gov:9418/pmc/python-pmc-ctxdecoextended.git
cd python-pmc-ctxdecoextended
pip install -r requirements/test.txt -e .
```

## Test

Test configuration is defined in the `tox.ini` file and includes `py.test` tests
and `flake8` source code checker.

You can run all of the tests:

```
python setup.py test
```

To run just the `py.test` tests, not `flake8`, and to re-use the current `virtualenv`:

```sh
py.test
```

## API

### Demo

```python
>>> from pmc.ctxdecoextended import demo_function
>>> demo_function(1)
1

```
