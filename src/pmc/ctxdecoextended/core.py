from contextlib import ContextDecorator, AbstractContextManager
from typing import Callable


class ContextDecoratorExtended(ContextDecorator, AbstractContextManager):
    """
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


    Example

        from pmc.ctxdecoextended import ContextDecoratorExtended

        class demo_ctx_decorator(ContextDecoratorExtended):
            def __init__(self, arg1=default_arg1_val, ..., kwarg1=default_kwarg1_val,...)
                pass
            def __enter__(self):
                return self
            def __exit__(self, e_type, e, e_tb):
                pass
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

    Notes

        You have to implement abstract methods __enter__ & __exit__
        to make your ContextDecoratorExtended derived class to work
        as decorator or context manager.
    """

    def __new__(cls, func: Callable = None, *args, **kwargs):
        # create decorator to be used in non functional form as `@try_catch_log`
        return cls(*args, **kwargs)(func) if func else object.__new__(cls)

    # def __call__(self, func: Callable, *args, **kwargs):
    #     # handle decorator in `@try_catch_log(...)` form
    #     self._fail_if_func_is_not_callable(func)
    #     return super().__call__(func)
    #
    # def __enter__(self, *args, **kwargs):
    #     """ Acquire a resource phase """
    #     return self
    #
    # def __exit__(self, e_type, e, e_tb):
    #     """ Release a resource phase """
    #     pass

    @staticmethod
    def _fail_if_func_is_not_callable(func):
        if func and not callable(func):
            raise ValueError(f"argument `func` must be callable, but `{repr( func )}` is given.")
