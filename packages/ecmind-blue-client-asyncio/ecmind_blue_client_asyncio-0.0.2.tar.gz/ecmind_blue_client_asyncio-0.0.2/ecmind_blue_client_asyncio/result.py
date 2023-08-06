from typing import List, Optional

from .param import Param
from .result_file import ResultFile

class ResultValues:
    def __init__(self, params: dict[str, Param]) -> None:
        self.params = params

    def __getitem__(self, key)->any:
        return self.params[key].value

class Result:
    """Result dataclass.

    values -- Dictionary of output parameters.
    files -- List of ResultFile() output file parameters.
    return_code -- Integer representation of the job result.
    error_message -- String containing error responses from the server on None if return_code is 0.
    client_infos -- List of optional data returned by the individual client implementation.
    """

    params: dict[str, Param]
    values: ResultValues
    files: List[ResultFile]
    return_code: int
    error_message: Optional[str] = None
    client_infos: Optional[dict] = None

    def __init__(self, params: dict[str, Param], files: List[ResultFile], return_code: int, error_message: Optional[str] = None, client_infos: Optional[dict] = None):
        self.params = params
        self.files = files
        self.return_code = return_code
        self.error_message = error_message
        self.client_infos = client_infos
        self.values = ResultValues(self.params)

    def __repr__(self):
        if self.return_code == 0:
            return f"Result (success, {len(self.files)} files): {self.values}"
        else:
            return f"Result (failed, code {self.return_code}): {self.error_message}"

    def __bool__(self):
        return self.return_code == 0 and self.error_message is None
