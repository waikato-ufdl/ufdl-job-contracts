from typing import TypeVar, Union

from ufdl.jobtypes.base import UFDLType

from ..params import TypeConstructor

TypesType = TypeVar('TypesType', bound=Union[UFDLType, TypeConstructor])
