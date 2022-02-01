from typing import Type

from ufdl.jobtypes.util import parse_args

from ..base import UFDLJobContract
from ..error import ContractParsingException
from ..initialise import name_type_translate


def parse_contract(contract_string: str) -> UFDLJobContract:
    if not isinstance(contract_string, str):
        raise ContractParsingException(str(contract_string), "Not a string")

    args_start = contract_string.find("<")
    if args_start == -1:
        name = contract_string.strip()
        args = ""
    else:
        name = contract_string[:args_start].strip()
        args = contract_string[args_start:].strip()

    contract_cls: Type[UFDLJobContract] = name_type_translate(name)

    if contract_cls is None:
        raise ContractParsingException(contract_string, f"Unknown contract-name \"{name}\"")

    try:
        type_args = parse_args(args)
        params = contract_cls.params()
    except Exception as e:
        raise ContractParsingException(contract_string, e) from e

    num_params = len(params)
    num_args = len(type_args)
    if num_args != num_params:
        raise ContractParsingException(contract_string, f"Expected {num_params} type-arguments but got {num_args}")

    try:
        return contract_cls(
            {
                param.name: type_arg
                for type_arg, param in zip(type_args, params)
            }
        )
    except Exception as e:
        raise ContractParsingException(contract_string, e) from e
