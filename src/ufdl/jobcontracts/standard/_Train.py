from typing import Dict

from ufdl.jobtypes.base import UFDLType
from ufdl.jobtypes.standard import Model, PK
from ufdl.jobtypes.standard.server import Dataset, Domain, Framework

from ..base import UFDLJobContract
from ..params import JobContractParamName, JobContractParams

train_params = JobContractParams()
DomainType = train_params.add_simple_param('DomainType', Domain)
FrameworkType = train_params.add_simple_param('FrameworkType', Framework)
ModelType = train_params.add_dependent_param('ModelType', Model, DomainType, FrameworkType)


class Train(UFDLJobContract, params=train_params):
    """
    Job contract for jobs which train a model from a dataset.
    """
    def __init__(self, types: Dict[JobContractParamName, UFDLType]):
        domain_type = types[DomainType]
        model_type = types[ModelType]

        dataset_pk_type = PK((Dataset((domain_type,)),))

        super().__init__(
            {"dataset": (dataset_pk_type,)},
            {"model": model_type}
        )

