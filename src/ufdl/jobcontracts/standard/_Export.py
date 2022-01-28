from ..base import UFDLJobContract
from ..params import JobContractParams

# Type parameters
params = JobContractParams()


class Export(
    UFDLJobContract,
    params=params,
    inputs={},
    outputs={}
):
    """
    A placeholder for the Export contract.
    """
    pass
