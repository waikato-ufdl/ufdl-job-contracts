from ufdl.jobtypes.standard import JobOutput, Model, PK
from ufdl.jobtypes.standard.server import Dataset, Domain, Framework

from ..base import UFDLJobContract
from ..params import JobContractParams, TypeConstructor

predict_params = JobContractParams()
DomainType = predict_params.add_simple_param('DomainType', Domain)
FrameworkType = predict_params.add_simple_param('FrameworkType', Framework)
ModelType = predict_params.add_dependent_param('ModelType', Model, DomainType, FrameworkType)

model_type_constructor = TypeConstructor.indirect_dependency(JobOutput, ModelType)
dataset_pk_type_constructor = TypeConstructor.indirect_dependency(
    PK,
    TypeConstructor.indirect_dependency(Dataset, DomainType)
)


class Predict(
    UFDLJobContract,
    params=predict_params,
    inputs={
        "model": (model_type_constructor,),
        "dataset": (dataset_pk_type_constructor,)
    },
    outputs={
        "predictions": dataset_pk_type_constructor
    }
):
    pass