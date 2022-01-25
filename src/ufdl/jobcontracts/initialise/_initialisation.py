import builtins
from typing import Dict, Optional, Union

from ufdl.jobtypes.error import NotInitialisedException

# Name/type mappings
NAME_TO_TYPE_MAP: Optional[Dict[str, type]] = None
TYPE_TO_NAME_MAP: Optional[Dict[type, str]] = None


def initialise_server(
        name_to_type_map: Dict[str, type]
):
    """
    Initialises the type-systems connection to the server.
    """
    global NAME_TO_TYPE_MAP, TYPE_TO_NAME_MAP
    from ..base import UFDLJobContract

    # Verify and reverse the name/type mapping
    NAME_TO_TYPE_MAP = {}
    TYPE_TO_NAME_MAP = {}
    for name, type in name_to_type_map.items():
        if not name.isidentifier():
            raise ValueError(f"Type-name '{name}' is not a valid Python identifier")
        if not isinstance(type, builtins.type) or not issubclass(type, UFDLJobContract):
            raise ValueError(f"Type must be a sub-class of {UFDLJobContract.__name__}")
        if type in TYPE_TO_NAME_MAP:
            raise ValueError(f"Multiple type-names detected for type {type}; mapping is not one-to-one")
        NAME_TO_TYPE_MAP[name] = type
        TYPE_TO_NAME_MAP[type] = name


def name_type_translate(name_or_type: Union[str, type]) -> Union[type, str, None]:
    """
    Translates a name into a type or vice-versa.

    :param name_or_type:
                The name or type to translate.
    :return:
                The name of the type or the type for the name.
                Returns None if no mapping is present.
    """
    global NAME_TO_TYPE_MAP, TYPE_TO_NAME_MAP
    mapping = NAME_TO_TYPE_MAP if isinstance(name_or_type, str) else TYPE_TO_NAME_MAP
    if mapping is None:
        raise NotInitialisedException()
    return mapping.get(name_or_type, None)
