from typing import Callable
import pytest
from pmc.ctxdecoextended import ContextDecoratorExtended
from functools import wraps


class demo_ctx_decorator(ContextDecoratorExtended):
    def __init__(self, multiply_by=2, suppress_warnings=False):
        self._multiply_by = multiply_by
        self._suppress_warnings = suppress_warnings

    def __call__(self, func: Callable, *args, **kwargs):
        self._fail_if_func_is_not_callable(func)

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


def test_cde_as_decorator():
    @demo_ctx_decorator
    def demo_function(a):
        return a

    assert demo_function(100) == 200


def test_cde_as_decorator_call():
    @demo_ctx_decorator(multiply_by=3)
    def demo_function(a):
        return a

    assert demo_function(101) == 303


def test_cde_as_decorating_function():
    def demo_function(a):
        return a

    decorated_func = demo_ctx_decorator(multiply_by=4)(demo_function)
    assert decorated_func(102) == 408

    decorated_func = demo_ctx_decorator(demo_function)
    assert decorated_func(-102) == -204


def test_cde_as_decorating_function_value_error():
    with pytest.raises(ValueError):
        demo_ctx_decorator(1)

    with pytest.raises(ValueError):
        demo_ctx_decorator("string")


def test_cde_as_ctx_manager_no_warnings():
    def demo_function(a):
        return a

    with demo_ctx_decorator(suppress_warnings=True):
        assert demo_function(104) == 104
        raise Warning("here is the warning")
        assert True


def test_cde_as_ctx_manager_with_warnings():
    def demo_function(a):
        return a

    with pytest.raises(Warning):
        with demo_ctx_decorator():
            assert demo_function(104) == 104
            raise Warning("here is the warning")
