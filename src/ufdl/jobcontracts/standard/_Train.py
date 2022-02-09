from ufdl.jobtypes.standard import Model, PK
from ufdl.jobtypes.standard.server import Dataset, Domain, Framework

from ..base import UFDLJobContract, Input, Output
from ..params import JobContractParams, TypeConstructor

train_params = JobContractParams()
DomainType = train_params.add_simple_param('DomainType', Domain())
FrameworkType = train_params.add_simple_param('FrameworkType', Framework())

model_type_constructor = TypeConstructor.indirect_dependency(
    Model,
    DomainType, FrameworkType
)
dataset_pk_type_constructor = TypeConstructor.indirect_dependency(
    PK,
    TypeConstructor.indirect_dependency(Dataset, DomainType)
)


class Train(
    UFDLJobContract,
    params=train_params,
    inputs={
        "dataset": Input(
            dataset_pk_type_constructor,
            help="The dataset to train the model on"
        )
    },
    outputs={
        "model": Output(
            model_type_constructor,
            help="The trained model"
        )
    }
):
    """
    Job contract for jobs which train a model from a dataset.
    """
    @property
    def dataset(self):
        return self.inputs['dataset']

    @property
    def model(self):
        return self.outputs['model']
