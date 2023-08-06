import sys
from functools import wraps
from typing import Dict, Type, Optional, Callable, Container


class ErrorWrapper:
    def __init__(
        self,
        error_mappings: Optional[Dict[Type[Exception], Type[Exception]]] = None,
        default_error: Optional[Type[Exception]] = None,
        skipped_errors: Optional[Container[Type[Exception]]] = None,
    ):
        from assimilator.core.database.exceptions import DataLayerError

        self.error_mappings = error_mappings or {}
        self.default_error = default_error
        self.skipped_errors = {
            *(skipped_errors or set()),
            KeyboardInterrupt,
            SystemExit,
            DataLayerError,
            *self.error_mappings.values(),  # we want to skip all the mapped values as they are already fixed
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Type[Exception], exc_val: Exception, exc_tb):
        if exc_val is None:
            return True
        elif any(issubclass(exc_type, error) for error in self.skipped_errors):
            return False

        wrapped_error = self.error_mappings.get(exc_type)
        _, _, tb = sys.exc_info()

        if wrapped_error is not None:
            raise wrapped_error(exc_val).with_traceback(tb)
        elif self.default_error is not None:
            raise self.default_error(exc_val).with_traceback(tb)

        return False   # No wrapping error was found

    def decorate(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        wrapper: func
        return wrapper

    def __str__(self):
        return f"{type(self).__name__}({self.error_mappings})"


__all__ = ['ErrorWrapper']
