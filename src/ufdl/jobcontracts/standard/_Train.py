from ufdl.jobtypes.standard import Model, PK
from ufdl.jobtypes.standard.server import Dataset, Domain, Framework

from ..base import UFDLJobContract
from ..params import JobContractParams, TypeConstructor

train_params = JobContractParams()
DomainType = train_params.add_simple_param('DomainType', Domain)
FrameworkType = train_params.add_simple_param('FrameworkType', Framework)
ModelType = train_params.add_dependent_param('ModelType', Model, DomainType, FrameworkType)

dataset_pk_type_constructor = TypeConstructor.indirect_dependency(
    PK,
    TypeConstructor.indirect_dependency(Dataset, DomainType)
)


class Train(
    UFDLJobContract,
    params=train_params,
    inputs={
        "dataset": (dataset_pk_type_constructor,)
    },
    outputs={
        "model": TypeConstructor.direct_dependency(ModelType)
    }
):
    """
    Job contract for jobs which train a model from a dataset.
    """
    pass

