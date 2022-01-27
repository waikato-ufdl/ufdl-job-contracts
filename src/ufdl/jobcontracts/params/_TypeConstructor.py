from typing import Dict, Iterator, List, Optional, Type, Union

from ufdl.jobtypes.base import UFDLType
from ufdl.jobtypes.initialise import name_type_translate
from ufdl.jobtypes.util import format_type, is_subtype, AnyUFDLType

from ._JobContractParamName import JobContractParamName


class TypeConstructor:
    """
    Class which has the ability to construct a specific type once its generic
    parameters are satisfied.
    """
    @classmethod
    def direct_dependency(cls, bound: JobContractParamName) -> 'TypeConstructor':
        return cls(bound)

    @classmethod
    def indirect_dependency(
            cls,
            bound: Type[UFDLType],
            *args: Union[AnyUFDLType, JobContractParamName, 'TypeConstructor']
    ) -> 'TypeConstructor':
        return TypeConstructor(bound, *args)

    def __init__(
            self,
            bound: Union[Type[UFDLType], JobContractParamName],
            *args: Union[AnyUFDLType, JobContractParamName, 'TypeConstructor']):
        if isinstance(bound, JobContractParamName):
            if len(args) > 0:
                raise ValueError("Cannot supply arguments to a parameter")
            self._bound_base: Optional[UFDLType] = None
        else:
            expected_base_types = bound.type_params_expected_base_types()
            num_args_supplied = len(args)
            num_args_expected = len(expected_base_types)
            if num_args_supplied != num_args_expected:
                raise ValueError(f"{format_type(bound)} expects {num_args_expected} args but received {num_args_supplied}")
            bound_base_args = []
            for arg, expected_base_type in zip(args, expected_base_types):
                if isinstance(arg, JobContractParamName):
                    bound_base_args.append(expected_base_type)
                elif isinstance(arg, TypeConstructor):
                    if arg._bound_base is None:
                        raise ValueError(f"Cannot supply a direct dependency ({arg.bound_str()}) to a type-constructor")
                    bound_base_args.append(arg._bound_base)
                else:
                    bound_base_args.append(arg)
            self._bound_base = bound(tuple(bound_base_args))

        self._bound = bound
        self._args = args

        # Generate the set of dependencies
        if isinstance(bound, JobContractParamName):
            self._dependencies = {bound}
        else:
            self._dependencies = set()
            for arg in args:
                if isinstance(arg, JobContractParamName):
                    self._dependencies.add(arg)
                elif isinstance(arg, TypeConstructor):
                    self._dependencies += set(arg.dependencies)

    @property
    def bound_base(self):
        return self._bound_base

    @property
    def dependencies(self) -> Iterator[JobContractParamName]:
        yield from self._dependencies

    def construct(self, types: Dict[JobContractParamName, AnyUFDLType]) -> AnyUFDLType:
        if isinstance(self._bound, JobContractParamName):
            return types[self._bound]

        return self._bound(
            tuple(
                types[arg] if isinstance(arg, JobContractParamName)
                else arg.construct(types) if isinstance(arg, TypeConstructor)
                else arg
                for arg in self._args
            )
        )

    def bound_str(self) -> str:
        if isinstance(self._bound, JobContractParamName):
            return str(self._bound)

        formatted_args = ", ".join(
            str(arg) if isinstance(arg, JobContractParamName)
            else arg.bound_str() if isinstance(arg, TypeConstructor)
            else format_type(arg)
            for arg in self._args
        )

        return f"{name_type_translate(self._bound)}<{formatted_args}>"

    def extract_dependency_type(
            self,
            dependency_name: Union[str, JobContractParamName],
            from_type: AnyUFDLType
    ) -> List[AnyUFDLType]:
        # Check the name is one of our dependencies
        if dependency_name not in self._dependencies:
            raise ValueError(f"{dependency_name} is not a dependency of {self.bound_str()}")

        # For a simple dependency, there is only one dependency name, and it matches the entire type
        if isinstance(self._bound, JobContractParamName):
            return [from_type]

        if not is_subtype(from_type, self._bound_base):
            raise ValueError(f"Type {from_type} is not constructable by {self.bound_str()}")

        results = []
        for from_type_type_arg, sub_bound in zip(from_type.type_args, self._args):
            if isinstance(sub_bound, JobContractParamName):
                if sub_bound == dependency_name:
                    results.append(from_type_type_arg)
            elif isinstance(sub_bound, TypeConstructor):
                results += sub_bound.extract_dependency_type(dependency_name, from_type_type_arg)

        return results
