from typing import Type

from ufdl.jobtypes.util import format_type

from ..base import UFDLJobContract
from ..initialise import name_type_translate


def format_contract_type(
        contract_type: Type[UFDLJobContract],
        *,
        include_io: bool = False
) -> str:
    if contract_type is UFDLJobContract:
        raise Exception(f"Can't format base contract class {UFDLJobContract.__qualname__}")

    contract_name = name_type_translate(contract_type)
    contract_params = contract_type.params()

    if not include_io:
        return f"{contract_name}{contract_params}"

    raise NotImplementedError()


def format_contract(
        contract: UFDLJobContract,
        *,
        include_io: bool = False
) -> str:
    if not include_io:
        return str(contract)

    inputs = ",\n".join(
        f"\t{input_name}: " + " | ".join(map(format_type, input.types))
        for input_name, input in contract.inputs.items()
    )

    outputs = ",\n".join(
        f"\t{output_name}: {format_type(output.type)}"
        for output_name, output in contract.outputs.items()
    )

    return f"{contract}(\n{inputs}\n) -> {{\n{outputs}\n}}"
