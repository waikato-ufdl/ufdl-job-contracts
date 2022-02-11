from abc import ABC
from typing import Dict

from ufdl.jobtypes.base import UFDLType
from ufdl.jobtypes.error import expect

from ..initialise import name_type_translate
from ..params import JobContractParams
from ._Input import Input
from ._InputConstructor import InputConstructor
from ._Output import Output
from ._OutputConstructor import OutputConstructor


class UFDLJobContract(ABC):
    """
    TODO
    """
    _params: JobContractParams
    _input_constructors: Dict[str, InputConstructor]
    _output_constructors: Dict[str, OutputConstructor]

    def __init_subclass__(cls, **kwargs):
        params = expect(JobContractParams, kwargs.pop('params'))
        input_constructors = expect(dict, kwargs.pop('inputs'))
        output_constructors = expect(dict, kwargs.pop('outputs'))

        for input_name, input_constructor in input_constructors.items():
            if not isinstance(input_name, str) or not input_name.isidentifier():
                raise ValueError("All input names must be valid identifiers")
            if not isinstance(input_constructor, InputConstructor):
                raise ValueError(f"Input '{input_name}' is not an {InputConstructor.__name__}")
            input_constructor._name = input_name

        for output_name, output_constructor in output_constructors.items():
            if not isinstance(output_name, str) or not output_name.isidentifier():
                raise ValueError("All output names must be valid identifiers")
            if not isinstance(output_constructor, OutputConstructor):
                raise ValueError(f"Output '{output_name}' is not an {OutputConstructor.__name__}")
            output_constructor._name = output_name

        cls._params = params
        cls._input_constructors = input_constructors
        cls._output_constructors = output_constructors

    @classmethod
    def params(cls):
        return cls._params

    @classmethod
    def input_constructors(cls):
        return cls._input_constructors

    @classmethod
    def output_constructors(cls):
        return cls._output_constructors

    @classmethod
    def contract_class_name(cls) -> str:
        name = name_type_translate(cls)
        if name is None:
            raise TypeError(f"No name translation for {cls}")
        return name

    @classmethod
    def format(cls):
        return f"{cls.contract_class_name()}{cls._params}"

    def __init__(
            self,
            types: Dict[str, UFDLType]
    ):
        # Make sure types really is a dict
        expect(dict, types)

        # Make sure all parameters are specified and are types
        for param_name in self._params.names():
            if param_name not in types:
                raise ValueError(f"Contract {self.format()} missing type-argument \"{param_name}\"")
            expect(UFDLType, types[param_name])

        # Make sure only the parameters are specified
        for name in types:
            if name not in self._params:
                raise ValueError(f"Contract {self.format()} given unknown type-argument \"{name}\"")

        # Attempting to fix all bounds will check for type correctness
        self.params().get_new_bounds_for_fixed(**{
            str(param_name): param_type
            for param_name, param_type in types.items()
        })

        inputs: Dict[str, Input] = {
            input_name: input_constructor.construct(types)
            for input_name, input_constructor in self._input_constructors.items()
        }

        outputs: Dict[str, Output] = {
            output_name: output_constructor.construct(types)
            for output_name, output_constructor in self._output_constructors.items()
        }

        self._inputs = inputs
        self._outputs = outputs
        self._types = types

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def types(self):
        return self._types

    def format_type_args(self) -> str:
        args = tuple(
            self._types[param.name]
            for param in self._params
        )

        if len(args) == 0:
            return ""

        return f"<{', '.join(str(arg) for arg in args)}>"

    def is_subtype_of(self, other: 'UFDLJobContract') -> bool:
        """
        Checks if this contract can be used in place of another contract.

        :param other:
                    The other contract to compare this one to.
        :return:
                    Whether this contract can be used in place of other.
        """
        return (
                type(self) is type(other)
                and all(
                    other_type.is_subtype_of(self_type)
                    for input_name in self.inputs.keys()
                    for self_type, other_type in zip(self.inputs[input_name].types, other.inputs[input_name].types)
                )
                and all(
                    self.outputs[output_name].type.is_subtype_of(other.outputs[output_name].type)
                    for output_name in self.outputs.keys()
                )
        )

    def __str__(self):
        return f"{self.contract_class_name()}{self.format_type_args()}"
