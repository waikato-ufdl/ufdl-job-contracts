from ufdl.jobtypes.standard import JobOutput, Model, PK, Name
from ufdl.jobtypes.standard.server import Dataset, Domain, Framework

from ..base import UFDLJobContract
from ..params import JobContractParams, TypeConstructor

# Type parameters
predict_params = JobContractParams()
DomainType = predict_params.add_simple_param('DomainType', Domain)
FrameworkType = predict_params.add_simple_param('FrameworkType', Framework)

# IO type constructors
model_type_constructor = TypeConstructor.indirect_dependency(
    JobOutput,
    TypeConstructor.indirect_dependency(Model, DomainType, FrameworkType)
)
dataset_type_constructor = TypeConstructor.indirect_dependency(Dataset, DomainType)
dataset_pk_type_constructor = TypeConstructor.indirect_dependency(
    PK,
    dataset_type_constructor
)
dataset_name_type_constructor = TypeConstructor.indirect_dependency(
    Name,
    dataset_type_constructor
)


class Predict(
    UFDLJobContract,
    params=predict_params,
    inputs={
        "model": (model_type_constructor,),
        "dataset": (dataset_pk_type_constructor, dataset_name_type_constructor)
    },
    outputs={
        "predictions": dataset_pk_type_constructor
    }
):
    pass