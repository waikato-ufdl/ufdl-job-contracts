from typing import Type

from ..base import UFDLJobContract
from ..initialise import name_type_translate


def format_contract_type(contract_type: Type[UFDLJobContract]) -> str:
    if contract_type is UFDLJobContract:
        raise Exception(f"Can't format base contract class {UFDLJobContract.__qualname__}")
    return f"{name_type_translate(contract_type)}{contract_type.params()}"
