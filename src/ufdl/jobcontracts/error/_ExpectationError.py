from typing import Type, TypeVar


class ExpectationError(Exception):
    """
    Class of exception for when the wrong type is passed to a function.
    """
    def __init__(self, expected_type: type, received_value):
        super().__init__(
            f"Expected {expected_type}, received: ({type(received_value)}) {received_value}"
        )


# TODO
ExpectedType = TypeVar('ExpectedType')


def expect(expected_type: Type[ExpectedType], received_value) -> ExpectedType:
    """
    TODO
    :param expected_type:
    :param received_value:
    :return:
    """
    if not isinstance(received_value, expected_type):
        raise ExpectationError(received_value, received_value)
    return received_value
