import logging
import socket
from random import randint

from .blue_exception import BlueException

from .job import Job
from .result import Result
from .job_caller import JobCaller


class BlueClient():
    @staticmethod
    def __encrypt_password(password: str) -> str:
        if password is None or password == "":
            raise ValueError("Password must not be empty")

        create_random_char = lambda: chr(ord("0") + (randint(0, 32000) % 8))

        plen = len(password)
        nmax = 4 * plen * 2
        ioff = randint(0, 32000) % max(1, nmax - plen * 3 - 3)
        cryptid = chr(ord("A") + plen) + chr(ord("A") + ioff)
        for _ in range(0, ioff):
            cryptid += create_random_char()

        replace_in_string = lambda i, c: cryptid[:i] + c + cryptid[i + 1 :]

        for i in range(0, plen):
            j = 2 + ioff + i * 3
            oct_part = ioff + ord(password[i])
            oct_data = f"{oct_part:03o}"
            for k in range(0, 3):
                cryptid = replace_in_string(j + k, oct_data[k])

        for i in range(2 + ioff + 3 * plen, nmax):
            cryptid = replace_in_string(i, create_random_char())

        try:
            cryptid.encode("ascii")
            return cryptid
        except ValueError as ex:
            logging.debug(ex)
            return BlueClient.__encrypt_password(password)

    async def __attach(self, username: str, password: str):
        session_attach_job = Job("krn.SessionAttach", Flags=0, SessionGUID="")
        session_attach_result = await self.execute(session_attach_job)
        self.session_guid = session_attach_result.values["SessionGUID"]

        session_properties_set_job = Job(
            "krn.SessionPropertiesSet",
            Flags=0,
            Properties="instname;statname;address",
            address=f"{socket.gethostbyname(socket.gethostname())}=dummy",
            instname=self.appname,
            statname=socket.gethostname(),
        )
        
        await self.execute(session_properties_set_job)

        session_login_job = Job(
            "krn.SessionLogin",
            Flags=0,
            UserName=username,
            UserPwd=BlueClient.__encrypt_password(password),
        )
        session_login_result = await self.execute(session_login_job)

        if session_login_result.values["Description"] is not None and session_login_result.values["Description"] != "":
            raise RuntimeError(f'Login error: {session_login_result.values["Description"]}')

    def __init__(
        self,
        hostname: str,
        port: int,
        appname: str,
        username: str,
        password: str,
        file_cache_byte_limit: int = 33554432,
        auto_reconnect: bool = True,
    ):
        self.session_guid = None
        self.job_caller = None
        self.hostname = hostname
        self.port = port
        self.appname = appname
        self.username = username
        self.password = password
        self.file_cache_byte_limit = file_cache_byte_limit
        self.auto_reconnect = auto_reconnect
        self.job_caller: JobCaller = None

    async def connect(self):
        if self.job_caller is not None:
            # try to close existing job_caller
            try:
                self.job_caller.close()
            except Exception as ex:
                logging.warning(ex)
            # remove job_caller reference
            self.job_caller = None

        self.job_caller = JobCaller(self.hostname, self.port, self.file_cache_byte_limit)
        await self.job_caller.open()
        await self.__attach(self.username, self.password)

    def __del__(self):
        try:
            self.job_caller.close()
        except Exception as ex:
            logging.error(ex)

    async def execute(self, job: Job) -> Result:
        """Send a job to the blue server (via TCP), execute it and return the response.

        Keyword arguments:
        job -- A previously created Job() object.
        """

        if self.auto_reconnect:
            if self.job_caller is None:
                # try to connect if current job_caller is None
                await self.connect()

            try:
                return await self.job_caller.execute(job)
            except ConnectionAbortedError as ex:
                # fetch connection closed exceptions and try to reconnect and execute again
                logging.warning(ex)
                await self.connect()
                return await self.execute(job)
        else:
            if self.job_caller is None:
                raise BlueException(-1, "JobCaller is None. Do you call connect() first?")

            result:Result = await self.job_caller.execute(job)
            if not result and job.raise_exception:
                raise BlueException(return_code=result.return_code, message=str(result.error_message))
            return result


class BlueConnection:
    def __init__(
        self,
        hostname: str,
        port: int,
        appname: str,
        username: str,
        password: str,
        file_cache_byte_limit: int = 33554432,
        auto_reconnect: bool = True,
    ):
        self.client = None
        self.hostname = hostname
        self.port = port
        self.appname = appname
        self.username = username
        self.password = password
        self.file_cache_byte_limit = file_cache_byte_limit
        self.auto_reconnect = auto_reconnect

    async def __aenter__(self):
        self.client = BlueClient(
            hostname=self.hostname,
            port=self.port,
            appname=self.appname,
            username=self.username,
            password=self.password,
            file_cache_byte_limit=self.file_cache_byte_limit,
            auto_reconnect=self.auto_reconnect,
        )
        await self.client.connect()
        return self.client

    async def __aexit__(self, type_name, value, traceback):
        self.client.__del__()

