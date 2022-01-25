from typing import Union

from ufdl.jobtypes.base import UFDLType
from ufdl.jobtypes.util import format_type

from ._JobContractParam import JobContractParam


class SimpleJobContractParam(JobContractParam):
    """
    TODO
    """
    def __init__(self, name: str, bound: Union[UFDLType, str, int]):
        super().__init__(name)
        self._bound: Union[UFDLType, str, int] = bound

    @property
    def bound(self):
        return self._bound

    def bound_str(self) -> str:
        return format_type(self._bound)
