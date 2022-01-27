from typing import TypeVar, Union

from ufdl.jobtypes.util import AnyUFDLType

from ..params import TypeConstructor

TypesType = TypeVar('TypesType', bound=Union[AnyUFDLType, TypeConstructor])
