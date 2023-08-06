import base64
from datetime import datetime
from struct import pack, unpack
from typing import Dict
from .const import ParamTypes
from .param import Param


# Job Parameters
def build_parameters(params: Dict[str, Param]) -> bytes:
    data_offset = 4 + (len(params) * 12)
    data_length = 0

    parameter_descriptions = b""
    parameter_datas = b""

    for param_name, param in params.items():
        name_offset = data_offset + data_length
        type_id = param.type.value
        value_offset = data_offset + data_length + len(param_name) + 1
        parameter_description = pack("!iii", name_offset, type_id, value_offset)

        name = param_name.encode("ascii")
        value: bytes = b""

        if param.type == ParamTypes.STRING:
            value = str(param.value).encode("UTF-8")
        if param.type == ParamTypes.INTEGER:
            value = str(param.value).encode("UTF-8")
        if param.type == ParamTypes.BOOLEAN:
            value = ("1" if param.value else "0").encode("UTF-8")
        if param.type == ParamTypes.DOUBLE:
            value = str(param.value).encode("UTF-8")
        if param.type == ParamTypes.DATE_TIME:
            if isinstance(param.value, datetime):
                value = param.value.strftime("%d.%m.%y %H:%M:%S").encode("UTF-8")
            else:
                value = str(param.value).encode("UTF-8")
        if param.type == ParamTypes.BASE64:
            if isinstance(param.value, (bytearray, bytes)):
                value = base64.b64encode(param.value)
            else:
                value = base64.b64encode(param.value.encode("UTF-8"))

        parameter_data = name + b"\0" + value + b"\0"
        data_length += len(parameter_data)
        parameter_descriptions += parameter_description
        parameter_datas += parameter_data

    params_length = pack("!i", len(params))

    return params_length + parameter_descriptions + parameter_datas


def parse_parameters(params_raw: bytes) -> Dict[str, Param]:
    parameters = {}
    # Read Parameter Count
    params_count = unpack(">i", params_raw[0:4])[0]

    for i in range(0, params_count):
        description_offset = 4 + (12 * i)
        name_offset = unpack(">i", params_raw[description_offset : description_offset + 4])[0]
        param_type = unpack(">i", params_raw[description_offset + 4 : description_offset + 8])[0]
        value_offset = unpack(">i", params_raw[description_offset + 8 : description_offset + 12])[0]

        value_offset_end = -1
        if i == params_count - 1:
            value_offset_end = len(params_raw) - 1
        else:
            value_offset_end = (
                unpack(
                    ">i",
                    params_raw[description_offset + 12 : description_offset + 16],
                )[0]
                - 1
            )

        name = str(params_raw[name_offset : value_offset - 1], "ascii")
        value = params_raw[value_offset:value_offset_end]

        infered_param: Param = None
        if param_type == ParamTypes.STRING.value:
            infered_param = Param(name, ParamTypes.STRING, str(value, "UTF-8"))
        elif param_type == ParamTypes.INTEGER.value:
            infered_param = Param(name, ParamTypes.INTEGER, int(value))
        elif param_type == ParamTypes.BOOLEAN.value:
            infered_param = Param(name, ParamTypes.BOOLEAN, bool(value))
        elif param_type == ParamTypes.DOUBLE.value:
            infered_param = Param(name, ParamTypes.DOUBLE, float(value))
        elif param_type == ParamTypes.DATE_TIME.value:
            infered_param = Param(name, ParamTypes.DATE_TIME, datetime(value))
        elif param_type == ParamTypes.BASE64.value:
            infered_param = Param(name, ParamTypes.BASE64, base64.b64decode(value).decode("UTF-8"))

        parameters[name] = infered_param

    return parameters


def build_call_job_parameters(method: str, internal_parameters: bytes, parameters: bytes, mode="C") -> bytes:
    return (
        (mode + method).encode("ascii")
        + b"\0"
        + pack("!i", len(internal_parameters))
        + internal_parameters
        + pack("!i", len(parameters))
        + parameters
    )


# File Header
def build_file_header(file_length: int, extension: str, magic="@ASSTREAM@", seperator1="@", seperator2="@") -> bytes:
    return (
        magic.encode("ascii")
        + f"{file_length:0>10}".encode("ascii")
        + seperator1.encode("ascii")
        + pack("!10s", extension.encode("ascii"))
        + seperator2.encode("ascii")
    )


def parse_file_header(data: bytes) -> tuple[int, str, str]:
    magic = data[:10].decode("ascii")
    file_length = int(data[10:20].decode("ascii"))
    seperator1 = data[20:21].decode("ascii")
    extension = data[21:31].decode("ascii").replace("\x11", "")
    seperator2 = data[31:32].decode("ascii")

    assert magic == "@ASSTREAM@", "Invalid magic"
    assert seperator1 == "@", "Invalid seperator1"
    assert seperator2 == "@", "Invalid seperator2"

    return file_length, extension, magic


# File Footer
def build_file_footer(seperator="@", dummy="0000000000", magic="@MAERTSSA") -> bytes:
    return (seperator + dummy + magic).encode("ascii")


def parse_file_footer(data: bytes) -> tuple[str, str, str]:
    seperator = data[:1].decode("ascii")
    dummy = data[1:11].decode("ascii")
    magic = data[11:20].decode("ascii")

    assert seperator == "@", "Invalid separator"
    assert dummy == "0000000000", "Invalid dummy"
    assert magic == "@MAERTSSA", "Invaid magic"

    return magic, dummy


# Job Header
def build_job_header(job_length: int, dummy1="L:", protocol="BIN", dummy2="-", version="v50", compression="N") -> bytes:
    return (
        (dummy1 + protocol + dummy2).encode("ascii")
        + pack("!10s", str(job_length).encode("ascii"))
        + (version + compression).encode("ascii")
    )


def parse_job_header(data: bytes) -> tuple[int, str, str, str]:
    dummy1 = data[:2].decode("ascii")
    protocol = data[2:5].decode("ascii")
    dummy2 = data[5:6].decode("ascii")
    job_length = int(data[6:16].decode("ascii"))
    version = data[16:19].decode("ascii")
    compression = data[19:20].decode("ascii")

    assert dummy1 == "L:", "Invalid dummy1"
    assert protocol == "BIN", "Invalid protocol"
    assert dummy2 == "-", "Invalid dummy2"
    assert version == "v50", "Invalid version"
    assert compression == "N", "Invaid compression"

    return job_length, protocol, version, compression
