from typing import IO, Union

from ufdl.jobtypes.standard import Model, PK, Name
from ufdl.jobtypes.standard.server import Dataset, Domain, Framework, DatasetInstance

from ..base import UFDLJobContract, Input, Output, InputConstructor, OutputConstructor
from ..params import JobContractParams, TypeConstructor

train_params = JobContractParams()
DomainType = train_params.add_simple_param('DomainType', Domain())
FrameworkType = train_params.add_simple_param('FrameworkType', Framework())

model_type_constructor = TypeConstructor.indirect_dependency(
    Model,
    DomainType, FrameworkType
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


class Train(
    UFDLJobContract,
    params=train_params,
    inputs={
        "dataset": InputConstructor(
            dataset_pk_type_constructor,
            help="The dataset to train the model on"
        )
    },
    outputs={
        "model": OutputConstructor(
            model_type_constructor,
            help="The trained model"
        )
    }
):
    """
    Job contract for jobs which train a model from a dataset.
    """
    @property
    def domain_type(self) -> Domain:
        return self.types[DomainType]

    @property
    def framework_type(self) -> Framework:
        return self.types[FrameworkType]

    @property
    def dataset(self) -> Input[DatasetInstance]:
        return self.inputs['dataset']

    @property
    def model(self) -> Output[Union[bytes, IO[bytes]]]:
        return self.outputs['model']
