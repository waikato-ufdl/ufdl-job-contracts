from typing import Dict

from ufdl.jobtypes import AnyUFDLType
from ufdl.jobtypes.standard import JobOutput, Model, PK
from ufdl.jobtypes.standard.server import Dataset, Domain, Framework

from ..base import UFDLJobContract
from ..params import JobContractParamName, JobContractParams

predict_params = JobContractParams()
DomainType = predict_params.add_simple_param('DomainType', Domain)
FrameworkType = predict_params.add_simple_param('FrameworkType', Framework)
ModelType = predict_params.add_dependent_param('ModelType', Model, DomainType, FrameworkType)


class Predict(UFDLJobContract, params=predict_params):
    def __init__(self, types: Dict[JobContractParamName, AnyUFDLType]):
        domain_type = types[DomainType]
        model_type = types[ModelType]

        dataset_pk_type = PK((Dataset((domain_type,)),))

        super().__init__(
            {"model": (JobOutput((model_type,)),), "dataset": (dataset_pk_type,)},
            {"predictions": dataset_pk_type}
        )
