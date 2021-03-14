from abc import ABC
import requests
from package.utils.api_loader import ApiLoader


class WebserverLoader(ApiLoader, ABC):
    """
    Receives data from web-server
    """
    def __init__(self, params: dict):
        """
        Initialization
        :param params: web-server connection parameters
        """
        super().__init__(params)

    @ApiLoader._exception_handler
    def get_statistics(self) -> dict:
        """
        Get statistics info
        :return : answer message
        """
        url = f"http://{self._host}:{self._port}/api/v1/statistics"
        content = {'Content-Type': 'application/json'}

        response = requests.get(url, headers=content)
        response.raise_for_status()

        return response.json()

    @ApiLoader._exception_handler
    def get_last_message(self) -> dict:
        """
        Get last message info
        :return : answer message
        """
        url = f"http://{self._host}:{self._port}/api/v1/last_message"
        content = {'Content-Type': 'application/json'}

        response = requests.get(url, headers=content)
        response.raise_for_status()

        return response.json()
