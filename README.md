# python-pmc-ctxdecoextended

## Description

This class is an extension of a contextlib.ContextDecorator
(enables a context manager to also be used as a decorator)
that adds an ability to use a decorator without calling
it with/without arguments as a function as following

    @decorator
        def func():
            pass

The original ContextDecorator requires you to use it as

    @decorator()
        def func():
            pass
Or

    decorated_func = demo_ctx_decorator(func)
Or
    decorated_func = demo_ctx_decorator()(func)

### Notes

You have to implement abstract methods __enter__ & __exit__
to make your ContextDecoratorExtended derived class to work
as decorator or context manager.


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

## Demo

```python
>>> from pmc.ctxdecoextended import ContextDecoratorExtended
>>> class demo_ctx_decorator(ContextDecoratorExtended):
...     def __enter__(self):
...         return self
...     def __exit__(self, e_type, e, e_tb):
...         pass
... 
>>> @demo_ctx_decorator
... def demo_decorated_function(a):
...     return a
... 
>>> demo_decorated_function(101)
101

```

## Other examples in pseudo python code.
    
    from pmc.ctxdecoextended import ContextDecoratorExtended

    
    class demo_ctx_decorator(ContextDecoratorExtended):
    def __init__(self, multiply_by=2, suppress_warnings=False):
        self._multiply_by = multiply_by
        self._suppress_warnings = suppress_warnings

    def __call__(self, func: Callable, *args, **kwargs):
        """ Decorator functionality """
        if func and not callable(func):
            raise ValueError(f"argument `func` must be callable, but `{repr( func )}` is given.")

        @wraps(func)
        def inner(*args, **kwds):
            with self:
                return self._multiply_by * func(*args, **kwds)

        return inner

    def __enter__(self, *args, **kwargs):
        """ Acquire a resource phase """
        return self

    def __exit__(self, e_type, e, e_tb):
        """ Release a resource phase """
        if self._suppress_warnings and isinstance(e, Warning):
            return True
            # return True if you want to suppress a thrown exception if any.
            # return None, False or do nothing if you want the exception if any to propagate.

    # Use with default arguments
    @demo_ctx_decorator
    def demo_function(...):
        pass

    # Use with your custom arguments
    @demo_ctx_decorator(...)
    def demo_function(...):
        pass

    # Use as a context manager
    def demo_function(...):
        with demo_ctx_decorator(...) as ctx:
            pass
    # Use as a decorating function with default arguments
    decorated_func = demo_ctx_decorator(func)
    # or
    decorated_func = demo_ctx_decorator()(func)

    # Use as a decorating function your custom arguments
    decorated_func = demo_ctx_decorator(...)(func)

