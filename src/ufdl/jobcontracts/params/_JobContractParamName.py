class JobContractParamName:
    """
    Because type-arguments can be string literals, this class differentiates between
    a string literal type and the value of a type-parameter (identified by name).
    """
    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return self._name
