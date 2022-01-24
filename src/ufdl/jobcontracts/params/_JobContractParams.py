from typing import Dict, Iterator, List, Set, Type, Union

from ufdl.jobtypes.base import UFDLType

from ._DependentJobContractParam import DependentJobContractParam
from ._JobContractParam import JobContractParam
from ._JobContractParamName import JobContractParamName
from ._SimpleJobContractParam import SimpleJobContractParam


class JobContractParams:
    """
    TODO
    """
    def __init__(self):
        self._params: Dict[str, JobContractParam] = {}

    def __getitem__(self, name: str):
        return self._params[name]

    def names(self) -> Iterator[str]:
        return iter(self._params.keys())

    def add_simple_param(self, name: str, bound: Union[UFDLType, Type[UFDLType], str, int]) -> JobContractParamName:
        self._check_name(name)
        param = SimpleJobContractParam(name, bound)
        self._params[name] = param
        return JobContractParamName(name)

    def add_dependent_param(
            self,
            name: str,
            bound: Type[UFDLType],
            *args: Union[UFDLType, str, int, JobContractParamName]
    ) -> JobContractParamName:
        self._check_name(name)

        args_parsed = [
            arg if not isinstance(arg, JobContractParamName) else self[str(arg)]
            for arg in args
        ]

        param = DependentJobContractParam(
            name,
            bound,
            *args_parsed
        )

        # Add the new param as a dependency of its dependents
        for arg in args_parsed:
            if isinstance(arg, JobContractParam):
                arg.add_dependent(param)

        self._params[name] = param

        return JobContractParamName(name)

    def _check_name(self, name: str):
        if name in self._params:
            raise ValueError(f"Parameter '{name}' already exists")

    def _linearise(self) -> List[JobContractParam]:
        """
        Linearises the parameters into a list so that parameters which a given parameter depends upon
        always come before it in the list.
        """
        linearised: List[JobContractParam] = []
        added: Set[JobContractParam] = set()
        search_next: Set[JobContractParam] = set()

        # All simple params have no dependencies
        for param in self._params.values():
            if isinstance(param, SimpleJobContractParam):
                linearised.append(param)
                search_next.add(param)

        while len(search_next) != 0:
            to_add: Set[JobContractParam] = set()
            for param in search_next:
                for dependent in param.dependents:
                    if dependent not in added:
                        to_add.add(dependent)

            for param in to_add:
                linearised.append(param)

            added += to_add
            search_next = to_add

        return linearised

    def __iter__(self):
        return iter(self._linearise())

    def __str__(self):
        linearised = self._linearise()

        if len(linearised) == 0:
            return ""

        return f"<{', '.join(str(param) for param in linearised)}>"