from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

R = TypeVar("R")


@runtime_checkable
class SupportsSetitem(Protocol):
    """A class with an abstract ``__setitem__`` method."""

    @abstractmethod
    def __setitem__(self, idx, value):
        ...
