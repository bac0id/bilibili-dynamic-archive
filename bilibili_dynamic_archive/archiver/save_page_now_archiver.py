import os

from save_page_now_api import SavePageNowApi

from ..config import HTTP_USER_AGENT
from .archiver import Archiver


class SavePageNowArchiver(Archiver):
    def save(self, url: str) -> bool:
        token = self.__get_token()
        api = SavePageNowApi(token=token, user_agent=HTTP_USER_AGENT)
        try:
            json = api.save(
                url=url,
                save_outlinks=True,
                save_errors=True,
                save_screenshot=True,
            )
            print(json)
            return self.__is_success(json)
        except Exception:
            return False

    def __get_token(self):
        access_key = os.getenv("SAVEPAGENOW_ACCESS_KEY")
        secret_key = os.getenv("SAVEPAGENOW_SECRET_KEY")
        token = f"{access_key}:{secret_key}"
        return token

    def __is_success(self, json: dict):
        if not json:
            return False

        status = json.get("status")
        if status == "error":
            return False

        # If status is not in json, then actual status may be "pending".
        # Should we consider it a success?
        return True
