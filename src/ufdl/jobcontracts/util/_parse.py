from typing import Type

from ufdl.jobtypes.util import parse_args

from ..base import UFDLJobContract
from ..error import ContractParsingException, UnknownContractNameException
from ..initialise import name_type_translate


def parse_contract(contract_string: str) -> UFDLJobContract:
    args_start = contract_string.find("<")
    if args_start == -1:
        name = contract_string.strip()
        args = ""
    else:
        name = contract_string[:args_start].strip()
        args = contract_string[args_start:].strip()

    contract_cls: Type[UFDLJobContract] = name_type_translate(name)

    if contract_cls is None:
        raise UnknownContractNameException(name)

    try:
        parsed_args = parse_args(args)
    except Exception as e:
        raise ContractParsingException(contract_string) from e

    params = contract_cls.params().__iter__()

    return contract_cls(
        {
            param.name: type_arg
            for type_arg, param in zip(parsed_args, params)
        }
    )
