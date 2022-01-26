class UnknownContractNameException(Exception):
    """
    Exception for when a contract is specified by name and no translation
    for that name exists.
    """
    def __init__(self, contract_name: str):
        super().__init__(f"Unknown contract '{contract_name}'")
