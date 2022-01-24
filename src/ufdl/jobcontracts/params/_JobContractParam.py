from abc import ABC, abstractmethod, abstractproperty
from typing import Iterator, List

from ufdl.jobcontracts.params import JobContractParamName


class JobContractParam(ABC):
    """
    TODO
    """
    def __init__(self, name: str):
        if not name.isidentifier():
            raise ValueError("Param names must be identifiers")
        self._name: str = name
        self._dependents: List[JobContractParam] = []

    @property
    def name(self) -> JobContractParamName:
        return JobContractParamName(self._name)

    @property
    def dependents(self) -> Iterator['JobContractParam']:
        return iter(self._dependents)

    @abstractmethod
    @property
    def bound_str(self) -> str:
        """
        Returns a string-representation of the bound of this parameter.
        """
        raise NotImplementedError(self.bound_str.__name__)

    def add_dependent(self, dependent: 'JobContractParam'):
        self._dependents.append(dependent)

    def __str__(self):
        return f"{self._name}: {self.bound_str}"