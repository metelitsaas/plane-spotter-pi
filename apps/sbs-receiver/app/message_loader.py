import json
from abc import ABC
import requests
from package.utils.api_loader import ApiLoader
from package.utils.functions import datetime_handler
from receiver import Receiver


class MessageLoader(ApiLoader, ABC):
    """
    Loads SBS-1 messages to web-server
    """
    def __init__(self, params: dict, receiver_params: dict):
        """
        Initialization
        :param params: web-server connection parameters
        :param receiver_params: receiver connection parameters
        """
        super().__init__(params)
        self._receiver = Receiver(receiver_params['host'], receiver_params['port'])

    def run(self) -> None:
        """
        Gets messages from receiver and loads it to web-server by API
        """
        for message in self._receiver.get_message():
            message_ser = json.dumps(message, default=datetime_handler)
            self._send_message(message_ser)

    @ApiLoader._exception_handler
    def _send_message(self, message: str) -> None:
        """
        Post message at web-server endpoint
        :param message: serialized message
        """
        url = f"http://{self._host}:{self._port}/api/v1/sbs-message"
        content = {'Content-Type': 'application/json'}

        response = requests.post(url, data=message, headers=content)
        response.raise_for_status()
