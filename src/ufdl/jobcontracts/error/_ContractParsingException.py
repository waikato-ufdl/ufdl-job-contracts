from typing import Any


class ContractParsingException(Exception):
    def __init__(self, contract_string: str, cause: Any = None):
        message = f"Error parsing contract-string \"{contract_string}\""
        if cause is not None:
            message += f": {cause}"
        super().__init__(message)
