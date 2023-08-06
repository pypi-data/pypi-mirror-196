import asyncio
import hashlib
import logging
import os
import pathlib
import ssl
from asyncio import StreamReader, StreamWriter
from struct import unpack
from tempfile import gettempdir
from typing import Dict, List, Optional
from uuid import uuid4

from . import job_serializer as serializer
from .blue_exception import BlueException
from .const import ParamTypes
from .job import Job
from .param import Param
from .result import Result
from .result_file import ResultFile, ResultFileType


class JobCaller:
    # default certificate
    cert = (
        "-----BEGIN CERTIFICATE-----\n"
        "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"
        "NA==\n-----END CERTIFICATE-----"
    )

    def __init__(
        self, hostname: str, port: Optional[int] = 4000, file_cache_byte_limit: Optional[int] = 33554432, cert: Optional[str] = None
    ):
        """
        :param str hostname: hostname or ip address
        :param int port: tcp server port. Default 4000
        :param int Limit value from which the files are cached locally. Default 32MB
        :param str cert: Certificate of the server. Default
        :return: job caller instance
        :rtype: JobCaller
        """
        self.hostname = hostname
        self.port = port
        self.file_cache_byte_limit = file_cache_byte_limit
        self.cert = cert if cert is not None else self.cert

        self.ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
        self.ssl_context.load_verify_locations(cadata=self.cert)

        self.reader: StreamReader = None
        self.writer: StreamWriter = None

    async def open(self):
        """
        Connect to server
        """
        reader, writer = await asyncio.open_connection(self.hostname, self.port, ssl=self.ssl_context)

        self.reader = reader
        self.writer = writer

    def close(self):
        """
        Disconnect from server
        """
        self.writer.close()

    async def execute(self, job: Job) -> Result:
        """
        Execute Job

        :param Job job: Job to Execute
        :return: return job result
        :rtype: Result
        """
        if self.reader is None or self.writer is None:
            raise BlueException(-1, "No connection available. Did you call open() before?")

        # Create internal parameter
        intern_params: Dict[str, Param] = {}
        intern_params["streams"] = Param("streams", ParamTypes.INTEGER, len(job.files))
        internal_parameters = serializer.build_parameters(intern_params)

        # create parameter
        parameters = serializer.build_parameters(job.params)

        # create request parameters
        request_parameters_binary = serializer.build_call_job_parameters(job.name, internal_parameters, parameters)

        # calculate digest of request parameters
        request_digest = hashlib.sha1()
        request_digest.update(request_parameters_binary)

        # create request headers
        request_header_binary = serializer.build_job_header(job_length=len(request_parameters_binary) + 20)

        # send request
        self.writer.write(request_header_binary)
        self.writer.write(request_parameters_binary)

        # for each file
        for file in job.files:
            # read file info
            with pathlib.Path(file) as path:
                size = path.stat().st_size
                extension = path.suffix[1:]

                # write file header
                request_file_header_binary = serializer.build_file_header(size, extension)

                self.writer.write(request_file_header_binary)
                request_digest.update(request_file_header_binary)

                # stream file
                file_stream = open(file, "rb")
                data = file_stream.read(1024)
                while data:
                    self.writer.write(data)
                    request_digest.update(data)
                    data = file_stream.read(1024)
                file_stream.close()

                # write fix file footer @0000000000@MAERTSSA
                request_file_footer_binary = serializer.build_file_footer()
                self.writer.write(request_file_footer_binary)

                request_digest.update(request_file_footer_binary)

        # send request digest
        self.writer.write(request_digest.digest())
        await self.writer.drain()

        # ----------------------------------------------------------------------
        # Start read response
        # ----------------------------------------------------------------------

        # read header
        job_length, _protocol, _version, _compression = serializer.parse_job_header(await self.reader.read(20))

        # read body
        response_digest = hashlib.sha1()

        parameter_length = job_length - 20
        body_raw = b""
        while len(body_raw) < parameter_length:
            body_raw += await self.reader.read(parameter_length - len(body_raw))

        response_digest.update(body_raw)

        response = self.__parse_response_body(body_raw)

        return_code = response["internal_parameters"]["return"].value
        error_message = None
        if return_code != 0:
            error_message = ""
            errors = response["errors"]
            for error in errors:
                error_message += error["message"] + "\n"

        result_values = response["parameters"]

        # parse file streams

        result_files: List[ResultFile] = []

        if "streams" in response["internal_parameters"]:
            streams = response["internal_parameters"]["streams"]
            for _ in range(0, int(streams.value)):
                header_raw = await self.reader.read(32)
                response_digest.update(header_raw)

                file_length, extension, _magic = serializer.parse_file_header(header_raw)

                to_file = file_length >= self.file_cache_byte_limit
                remainder = file_length
                file_pointer = None
                byte_array = None
                file_path = None
                file_name = f"ecmind_{str(uuid4())}.{extension}"
                if to_file:
                    file_path = os.path.join(gettempdir(), file_name)
                    file_pointer = open(file_path, "wb")
                else:
                    byte_array = bytearray()
                buffer_size = 4096
                while remainder > 0:
                    file_part: bytes = await self.reader.read(min(remainder, buffer_size))
                    response_digest.update(file_part)
                    remainder -= len(file_part)
                    if to_file:
                        file_pointer.write(file_part)
                    else:
                        byte_array += bytearray(file_part)

                if to_file:
                    file_pointer.close()
                    result_file = ResultFile(
                        result_file_type=ResultFileType.FILE_PATH,
                        file_name=file_name,
                        file_path=file_path,
                    )
                else:
                    result_file = ResultFile(
                        result_file_type=ResultFileType.BYTE_ARRAY,
                        file_name=file_name,
                        byte_array=bytes(byte_array),
                    )

                result_files.append(result_file)

                footer_raw = await self.reader.read(20)
                response_digest.update(footer_raw)
                _magic, _dummy = serializer.parse_file_footer(footer_raw)

        response_digest_received = response_digest.digest()
        response_digest_expected = await self.reader.read(20)

        if response_digest_received != response_digest_expected:
            raise BlueException(-1, "Digest for response does not match.")

        return Result(result_values, result_files, return_code, error_message)

    def __parse_response_body(self, body_raw) -> Dict:
        result = {}

        # Read Mode
        mode = unpack("s", body_raw[0:1])[0]  # Always R

        logging.debug("Mode is %s", mode)
        body_raw = body_raw[1:]  # drop bytes

        # Read Internal Parameters
        internal_length = unpack(">i", body_raw[0:4])[0]  # read byte length of internal parameters
        body_raw = body_raw[4:]  # drop bytes

        internal_raw = body_raw[:internal_length]  # slice internal parameters
        body_raw = body_raw[internal_length:]  # drop bytes

        result["internal_parameters"] = serializer.parse_parameters(internal_raw)

        # Read Parameters
        params_length = unpack(">i", body_raw[0:4])[0]  # read byte length of parameters
        body_raw = body_raw[4:]  # drop bytes

        params_raw = body_raw[:params_length]  # slice parameters
        body_raw = body_raw[params_length:]  # drop bytes

        result["parameters"] = serializer.parse_parameters(params_raw)

        # Read Errors
        error_length = unpack(">i", body_raw[0:4])[0]  # read byte length of errors
        logging.debug("Error length is %s", error_length)
        error_raw = body_raw[4:]  # drop bytes

        result["errors"] = self.__parse_errors(error_raw)

        return result

    def __parse_errors(self, errors_raw) -> List[Dict]:
        errors = []
        # Read Parameter Count
        error_count = unpack(">i", errors_raw[0:4])[0]
        errors_raw = errors_raw[4:]  # drop bytes

        # dummy
        dummy = unpack(">i", errors_raw[0:4])[0]
        errors_raw = errors_raw[4:]  # drop bytes

        descriptions = []

        for _ in range(0, error_count):
            (
                message_length,
                source_code,
                source_name_length,
                error_code,
                info_elements_length,
            ) = unpack(">iiiii", errors_raw[0:20])
            errors_raw = errors_raw[20:]  # drop bytes

            info_elements = []
            for _ in range(0, info_elements_length):
                info_elements.append(unpack(">i", errors_raw[0:4])[0])
                errors_raw = errors_raw[4:]  # drop bytes

            descriptions.append(
                {
                    "message_length": message_length,
                    "source_code": source_code,
                    "source_name_length": source_name_length,
                    "error_code": error_code,
                    "info_elements_length": info_elements_length,
                    "info_elements": info_elements,
                }
            )

        for description in descriptions:
            message = str(errors_raw[: description["message_length"]], "utf-8")
            errors_raw = errors_raw[description["message_length"] :]  # drop bytes

            source = str(errors_raw[: description["source_name_length"]], "utf-8")
            errors_raw = errors_raw[description["source_name_length"] :]  # drop bytes

            infos = []
            for info_element in description["info_elements"]:
                info = str(errors_raw[:info_element], "utf-8")
                infos.append(info)
                errors_raw = errors_raw[info_element:]

            errors.append(
                {
                    "message": message,
                    "source_code": description["source_code"],
                    "source": source,
                    "error_code": description["error_code"],
                    "infos": infos,
                }
            )

        return errors
