from typing import Type, Union

from ufdl.jobtypes import AnyUFDLType
from ufdl.jobtypes.base import UFDLType
from ufdl.jobtypes.initialise import name_type_translate
from ufdl.jobtypes.util import format_type

from ._JobContractParam import JobContractParam


class DependentJobContractParam(JobContractParam):
    """
    TODO
    """
    def __init__(self, name: str, bound: Type[UFDLType], *bound_args: Union[AnyUFDLType, JobContractParam]):
        super().__init__(name)
        self._bound = bound
        self._bound_args = bound_args

        # Check the bound args have at least one degree of freedom
        type_params_expected_base_types = bound.type_params_expected_base_types()

    def bound_str(self) -> str:
        args = (
            "" if len(self._bound_args) == 0
            else f"<{', '.join(str(arg.name) if isinstance(arg, JobContractParam) else format_type(arg) for arg in self._bound_args)}>"
        )
        return f"{name_type_translate(self._bound)}{args}"
