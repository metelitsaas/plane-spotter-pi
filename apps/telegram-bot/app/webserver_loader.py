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
    def get_status(self) -> str:
        """
        Get system status
        :return : answer message
        """
        url = f"http://{self._host}:{self._port}/api/v1/status"
        content = {'Content-Type': 'text/plain'}

        response = requests.get(url, headers=content)
        response.raise_for_status()

        return response.text

    @ApiLoader._exception_handler
    def get_emergency(self) -> str:
        """
        Get emergency messages
        :return : answer message
        """
        return "PLUG"
