from collections import OrderedDict
from typing import Dict, Iterable, Iterator, Optional, Tuple, Type, Union

from ufdl.jobtypes.base import UFDLType
from ufdl.jobtypes.util import is_subtype, format_type, AnyUFDLType

from ._JobContractParam import JobContractParam
from ._JobContractParamName import JobContractParamName
from ._TypeConstructor import TypeConstructor


class JobContractParams(Iterable[JobContractParam]):
    """
    TODO
    """
    def __init__(self):
        self._params: OrderedDict[str, JobContractParam] = OrderedDict()

    def __getitem__(self, name: Union[JobContractParamName, str]):
        if isinstance(name, JobContractParamName):
            name = str(name)
        return self._params[name]

    def names(self) -> Iterator[str]:
        return iter(self._params.keys())

    def add_simple_param(self, name: str, bound: AnyUFDLType) -> JobContractParamName:
        return self.add_param(name, bound)

    def add_direct_param(self, name: str, bound: JobContractParamName):
        self.add_param(name, TypeConstructor(bound))

    def add_dependent_param(
            self,
            name: str,
            bound: Type[UFDLType],
            *args: Union[AnyUFDLType, JobContractParamName, TypeConstructor]
    ) -> JobContractParamName:
        return self.add_param(name, TypeConstructor(bound, *args))

    def add_param(self, name: str, bound: Union[AnyUFDLType, TypeConstructor]):
        if name in self._params:
            raise ValueError(f"Parameter '{name}' already exists")

        # Create the bound base type
        bound_base = (
            bound if not isinstance(bound, TypeConstructor) else
            bound.construct({
                param.name: param.bound_base
                for param in self._params.values()
            })
        )

        param = JobContractParam(
            name,
            bound,
            bound_base
        )

        # Add the new param as a dependency of its dependents
        for dependency in param.dependencies:
            self[dependency].add_dependent(name)

        self._params[name] = param

        return JobContractParamName(name)

    def get_new_bounds_for_fixed(self, **fixes: AnyUFDLType) -> Dict[str, Tuple[AnyUFDLType, Optional[AnyUFDLType]]]:
        """
        Given a number of 'fixes' (a fixed type for a type-parameter, returns a dictionary from
        each type parameter to the (lower, upper) boundary types that the type parameter can take
        without violating the 'fixes'.

        :param fixes:
                    The parameters to fix the types of.
        :return:
                    The (lower, upper) boundary types for all parameters.
        """
        # Use the current bounds as a starting point
        fixed_bounds = {
            param_name: (param.bound_base, None)
            for param_name, param in self._params.items()
        }

        # Process each fix in turn
        for param_name, fix in fixes.items():
            if param_name not in fixed_bounds:
                raise ValueError(f"Can't fix unknown parameter '{param_name}'")

            # Fix the specified parameter to the given fix-type
            self._update_fixed_bounds(fixed_bounds, param_name, fix, fix)

            # Get the parameter being fixed
            fixed_param = self[param_name]

            # Update the bounds on each dependent parameter
            self._update_dependents(fixed_bounds, fixed_param)

            # Update the bounds on each parameter we depend on
            self._update_dependencies(fixed_bounds, fixed_param)

        return fixed_bounds

    def _update_dependents(
            self,
            fixed_bounds: Dict[str, Tuple[AnyUFDLType, Optional[AnyUFDLType]]],
            param: JobContractParam
    ):
        for dependent_param_name in param.dependents:
            dependent_param = self[dependent_param_name]
            dependent_param_bound = dependent_param.bound
            assert isinstance(dependent_param_bound, TypeConstructor)
            self._update_fixed_bounds(
                fixed_bounds,
                dependent_param_name,
                dependent_param_bound.construct({
                    JobContractParamName(name): bounds[0]
                    for name, bounds in fixed_bounds.items()
                }),
                None
            )
            self._update_dependents(fixed_bounds, dependent_param)

    def _update_dependencies(
            self,
            fixed_bounds: Dict[str, Tuple[AnyUFDLType, Optional[AnyUFDLType]]],
            param: JobContractParam
    ):
        param_bound = param.bound
        assert isinstance(param.bound, TypeConstructor)
        for dependency_param_name in param.dependencies:
            dependency_param = self[dependency_param_name]
            fix_types = param_bound.extract_dependency_type(dependency_param_name, fixed_bounds[str(param.name)][0])
            for fix_type in fix_types:
                self._update_fixed_bounds(
                    fixed_bounds,
                    str(dependency_param_name),
                    None,
                    fix_type
                )

            self._update_dependencies(fixed_bounds, dependency_param)

    @staticmethod
    def _update_fixed_bounds(
            fixed_bounds: Dict[str, Tuple[AnyUFDLType, Optional[AnyUFDLType]]],
            param_name: str,
            new_lower_bound: Optional[AnyUFDLType],
            new_upper_bound: Optional[AnyUFDLType]
    ):
        current_lower_bound, current_upper_bound = fixed_bounds[param_name]

        if new_lower_bound is None or is_subtype(current_lower_bound, new_lower_bound):
            new_lower_bound = current_lower_bound
        elif not is_subtype(new_lower_bound, current_lower_bound):
            raise ValueError(f"Incompatible lower bounds {format_type(new_lower_bound)} and {format_type(current_lower_bound)}")

        if current_upper_bound is None:
            pass
        elif new_upper_bound is None or is_subtype(new_upper_bound, current_upper_bound):
            new_upper_bound = current_upper_bound
        elif not is_subtype(current_upper_bound, new_upper_bound):
            raise ValueError(f"Incompatible upper bounds {format_type(new_upper_bound)} and {format_type(current_upper_bound)}")

        if new_upper_bound is not None and not is_subtype(new_upper_bound, new_lower_bound):
            raise ValueError(f"Bounds crossed: {format_type(new_upper_bound)} is not a sub-type of {format_type(new_lower_bound)}")

        fixed_bounds[param_name] = (new_lower_bound, new_upper_bound)

    def __len__(self):
        return len(self._params)

    def __iter__(self):
        return iter(self._params.values())

    def __str__(self):
        if len(self) == 0:
            return ""

        return f"<{', '.join(str(param) for param in self)}>"