from typing import Iterator, List, Union

from ufdl.jobtypes import AnyUFDLType
from ufdl.jobtypes.util import format_type

from ._JobContractParamName import JobContractParamName
from ._TypeConstructor import TypeConstructor


class JobContractParam:
    """
    TODO
    """
    def __init__(
            self,
            name: str,
            bound: Union[AnyUFDLType, TypeConstructor],
            bound_base: AnyUFDLType
    ):
        if not name.isidentifier():
            raise ValueError("Parameter names must be identifiers")

        self._name: str = name
        self._bound = bound
        self._bound_base = bound_base

        self._dependents: List[str] = []

    @property
    def bound(self) -> Union[AnyUFDLType, TypeConstructor]:
        return self._bound

    @property
    def bound_base(self) -> AnyUFDLType:
        """
        Gets the base type of the bound of this parameter.
        """
        return self._bound_base

    @property
    def name(self) -> JobContractParamName:
        return JobContractParamName(self._name)

    @property
    def dependents(self) -> Iterator[str]:
        return iter(self._dependents)

    @property
    def dependencies(self) -> Iterator[JobContractParamName]:
        if isinstance(self._bound, TypeConstructor):
            yield from self._bound.dependencies

    def bound_str(self) -> str:
        """
        Returns a string-representation of the bound of this parameter.
        """
        return (
            self._bound.bound_str() if isinstance(self._bound, TypeConstructor)
            else format_type(self._bound)
        )

    def add_dependent(self, dependent: str):
        self._dependents.append(dependent)

    def __str__(self):
        return f"{self._name}: {self.bound_str()}"
