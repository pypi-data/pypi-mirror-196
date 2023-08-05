import logging

from datetime import datetime
from json import loads

from catwalk_common import CommonCaseFormat
from pydantic import error_wrappers

from catwalk_client.tools import CaseBuilder, CaseExporter
from catwalk_client.common import CatwalkHTTPClient


logger = logging.getLogger("catwalk_client")
logging.basicConfig(level=logging.INFO)


class CatwalkClient:
    def __init__(
        self,
        submitter_name: str = None,
        submitter_version: str = None,
        catwalk_url: str = None,
        auth_token: str = None,
        insecure: bool = True,
    ):
        self.http_client = CatwalkHTTPClient(catwalk_url, auth_token, insecure)
        self.submitter_name = submitter_name
        self.submitter_version = submitter_version

    def __setattr__(self, __name, __value):
        if __name != "http_client" and __name in self.http_client.__dict__.keys():
            logger.warn(
                f" [DEPRECATED] Usage of 'CatwalkClient.{__name}=<value>' is DEPRECATED. Please use 'set_{__name}' method!"
            )
            self.http_client.__dict__[__name] = __value

        self.__dict__[__name] = __value

    def set_auth_token(self, auth_token: str):
        self.http_client.auth_token = auth_token

    def set_catwalk_url(self, catwalk_url: str):
        self.http_client.catwalk_url = catwalk_url

    def set_insecure(self, insecure: bool):
        self.http_client.insecure = insecure

    def new_case(self) -> CaseBuilder:
        return CaseBuilder(client=self)

    def send(self, case_id: str, case: dict):
        try:
            case = CommonCaseFormat(
                submitter={
                    "name": self.submitter_name,
                    "version": self.submitter_version,
                },
                case_id=case_id,
                **case,
            )

            response, success = self.http_client.post("/api/cases/collect", case.json())

            if success:
                case_id = loads(response)["id"]
                logger.info(f" Collected catwalk case: {case_id}")
            else:
                logger.error(response)
        except error_wrappers.ValidationError as ex:
            logger.error(f" ValidationError: \n{ex}")
        except Exception as ex:
            logger.error(f" {type(ex).__name__}: \n{str(ex)}")

    def export_cases(
        self,
        from_datetime: datetime,
        to_datetime: datetime,
        submitter_name: str = None,
        submitter_version: str = None,
        max_retries: int = 5,
    ):
        exporter = CaseExporter(
            http_client=self.http_client,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            submitter_name=submitter_name or self.submitter_name,
            submitter_version=submitter_version or self.submitter_version,
            max_retries=max_retries,
        )
        yield from exporter.export()
