from typing import IO, Union

from ufdl.jobtypes.standard import JobOutput, Model, PK, Name
from ufdl.jobtypes.standard.server import Dataset, Domain, Framework
from wai.json.raw import RawJSONObject

from ..base import Input, Output, UFDLJobContract, InputConstructor, OutputConstructor
from ..params import JobContractParams, TypeConstructor

# Type parameters
predict_params = JobContractParams()
DomainType = predict_params.add_simple_param('DomainType', Domain())
FrameworkType = predict_params.add_simple_param('FrameworkType', Framework())

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
        "model": InputConstructor(
            model_type_constructor,
            help="The model to use to generate predictions"
        ),
        "dataset": InputConstructor(
            dataset_pk_type_constructor,
            dataset_name_type_constructor,
            help="The dataset to generate predictions for"
        )
    },
    outputs={
        "predictions": OutputConstructor(
            dataset_pk_type_constructor,
            help="The dataset containing the predictions"
        )
    }
):
    @property
    def domain_type(self) -> Domain:
        return self.types[DomainType]

    @property
    def framework_type(self) -> Framework:
        return self.types[FrameworkType]

    @property
    def model(self) -> Input[Union[bytes, IO[bytes]]]:
        return self.inputs['model']

    @property
    def dataset(self) -> Input[RawJSONObject]:
        return self.inputs['dataset']

    @property
    def predictions(self) -> Output[int]:
        return self.outputs['predictions']
