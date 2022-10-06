import inspect
from typing import Protocol, Callable
from abc import abstractmethod
from functools import cached_property


class BaseKeyBuilder(Protocol):
    func: Callable

    @abstractmethod
    def build(self, args: tuple, kwargs: dict, separator: str = ":", template_args: tuple = None) -> str:
        raise NotImplementedError


class KeyBuilder(BaseKeyBuilder):

    def __init__(self, func: Callable):
        self.func = func

    def build(self, args: tuple, kwargs: dict, separator: str = ":", template_args: tuple = None) -> str:
        func_params = list(self._get_func_params())
        key = f"{self.func.__module__}{separator}{self.func.__name__}"
        if func_params and func_params[0] == "self":
            key = f"{self.func.__module__}{separator}{self.func.__qualname__}"
        signature = self._func_signature.bind(*args, **kwargs)
        signature.apply_defaults()
        for _name, _value in signature.arguments.items():
            if template_args:
                if _name in template_args:
                    key += f"{separator}{_name}{separator}{_value}"
            else:
                key += f"{separator}{_name}{separator}{_value}"
        return key

    def _get_func_params(self):
        signature = self._func_signature
        for param_name in signature.parameters.keys():
            yield param_name

    @cached_property
    def _func_signature(self) -> inspect.Signature:
        return inspect.signature(self.func)
