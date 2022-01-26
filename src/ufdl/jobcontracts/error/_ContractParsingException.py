class ContractParsingException(Exception):
    def __init__(self, contract_string: str):
        super().__init__(f"Error parsing contract-string '{contract_string}'")
