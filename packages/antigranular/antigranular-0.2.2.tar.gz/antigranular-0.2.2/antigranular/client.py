"""
Module for AGClient class.

AGClient class contians all the methods to interact with the AG server like creating a session, uploading results, etc.
It also contains methods to get the budget, privacy odometer, etc.

"""

import requests
import json
from typing import Union
import warnings

from .magics.magics import AGMagic
from .enclave_client.oblv_client import get_oblv_client, oblv_client
from .config import config
from .models.models import AGServerInfo


def login(
    user_id: str,
    user_secret: str,
    competition: str = None,
    dataset: str = None,
):
    """
    Login to the AG server and get the client objects.

    Parameters:
        ag_client_id (str): The AG client ID.
        ag_client_secret (str): The AG client secret.
        competition (str, optional): The competition dataset ID.
        dataset (str, optional): The dataset ID.

    Returns:
        AGClient: The AGClient object.

    Raises:
        ConnectionError: If there is an error while creating the client.
    """
    try:
        return AGClient(user_id, user_secret, competition, dataset)
    except Exception as err:
        print(
            f"Login failed. Please verify the competition name and your credentials. If issue persists, contact support. Error: {str(err)}"
        )


class AGClient:
    """
    AGClient class to interact with the AG server for competitions as well as accessing datasets for functionalities like creating a session, uploading competition submissions, downloading metadata, etc.
    """

    oblv_enclave: oblv_client.Enclave
    session_id: str

    def __init__(self, ag_client_id, ag_client_secret, competition=None, dataset=None):
        """
        Initialize AGClient class and check for mock headers if MockClient.

        Parameters:
            ag_client_id (str): The AG client ID.
            ag_client_secret (str): The AG client secret.
            competition (str, optional): The competition dataset ID. Defaults to None.
            dataset (str, optional): The dataset ID. Defaults to None.

        Raises:
            ConnectionError: If there is an error while connecting to the server.
        """

        # Fetch latest PCRs from AG Server, and verify client version
        try:
            self._validate_server_info()
        except Exception as err:
            warnings.warn(f"Error while validating server info: {str(err)}")

        self.oblv_enclave = get_oblv_client(ag_client_id, ag_client_secret)
        self.headers = {}

        # Create an AG session
        self.connect(competition=competition, dataset=dataset)
        print(f"Connected to Antigranular server session id: {str(self.session_id)}")

        try:
            res = AGMagic.load_ag_magic()
        except Exception as ex:
            print(
                "Error loading %%ag magic functions, you might not be able to use cell magics as intended: ",
                str(ex),
            )

        AGMagic.load_oblv_client(self.oblv_enclave, self.session_id)

    def _validate_server_info(self) -> None:
        """
        Get the PCR values to use from antigranular.com.
        PCRs are fed to the enclave client for PCR validation along with client version check.
        """
        try:
            res = requests.get(config.AG_SRV_INFO_URL)
        except Exception as err:
            warnings.warn(f"Error fetching server AG information: {str(err)}")
        else:
            if res.status_code != 200:
                warnings.warn(
                    f"Error while getting PCR values from antigranular.com status code: {res.status_code} message: {res.text}"
                )
            ag_server_info = AGServerInfo.parse_raw(res.text)

            # Update the PCR values from the response
            config.AG_PCRS = ag_server_info.AG_PCRs.dict()
            from . import __version__

            if __version__ not in ag_server_info.supported_clients:
                warnings.warn(
                    f"Antigranular client version {__version__} not in supported clients list shared by the server, please update antigranular client to the latest version."
                )

    def connect(self, dataset: str = "", competition: str = "") -> None:
        """
        Connect to the AG server and create a session.

        Parameters:
            dataset (str, optional): The dataset ID. Defaults to "".
            competition (str, optional): The competition dataset ID. Defaults to "".

        Raises:
            ConnectionError: If there is an error while connecting to the server.
        """
    
        if not (dataset or competition):
            raise ValueError("dataset name or competition name must be provided.")
        if competition and dataset:
            raise ValueError(
                "Both competition and dataset cannot be passed. Please pass only one of them."
            )
        try:
            if competition:
                res = self._exec(
                    "POST",
                    "/start-session",
                    headers=self.headers,
                    json={
                        "session_type": "competition",
                        "type_identifier": competition,
                    },
                )
            if dataset:
                res = self._exec(
                    "POST",
                    "/start-session",
                    headers=self.headers,
                    json={"session_type": "dataset", "type_identifier": dataset},
                )
        except Exception as err:
            raise ConnectionError(f"Error calling /start-session: {str(err)}")
        else:
            if res.status_code != 200:
                raise requests.exceptions.HTTPError(
                    f"Error while starting a new session in enclave status code: {res.status_code} message: {res.text}"
                )
            self.session_id = json.loads(res.text)["session_id"]


    def interrupt_kernel(self) -> dict:
        """
        Interrupt the current session.

        Returns:
            dict: The interrupt kernel response.

        Raises:
            ConnectionError: If there is an error while calling /interrupt-kernel.
            requests.exceptions.HTTPError: If there is an error while fetching the interrupt kernel.
        """
        try:
            res = self._exec(
                "POST",
                "/sessions/interrupt-kernel",
                headers=self.headers,
                json={"session_id": self.session_id},
            )
        except Exception as e:
            raise ConnectionError(f"Error calling /terminate-session: {str(e)}")
        else:
            if res.status_code != 200:
                raise requests.exceptions.HTTPError(
                    f"Error while fetching the terminate-session, HTTP status code: {res.status_code}, message: {res.text}"
                )
            return json.loads(res.text)

    def terminate_session(self) -> dict:
        """
        Terminate the current session.

        Returns:
            dict: The terminate session response.

        Raises:
            ConnectionError: If there is an error while calling /terminate-session.
            requests.exceptions.HTTPError: If there is an error while fetching the terminate session.
        """
        try:
            res = self._exec(
                "POST",
                "/sessions/terminate-session",
                headers=self.headers,
                json={"session_id": self.session_id},
            )
        except Exception as e:
            raise ConnectionError(f"Error calling /terminate-session: {str(e)}")
        else:
            if res.status_code != 200:
                raise requests.exceptions.HTTPError(
                    f"Error while fetching the terminate-session, HTTP status code: {res.status_code}, message: {res.text}"
                )
            return json.loads(res.text)

    def privacy_odometer(self) -> dict:
        """
        Get the privacy odometer.

        Returns:
            dict: The privacy odometer.

        Raises:
            ConnectionError: If there is an error while calling /privacy_odometer.
            requests.exceptions.HTTPError: If there is an error while fetching the privacy odometer.
        """
        try:
            res = self._exec(
                "GET",
                "/sessions/privacy_odometer",
                params={"session_id": self.session_id},
                headers=self.headers,
            )
        except Exception as e:
            raise ConnectionError(f"Error calling /privacy_odometer: {str(e)}")
        else:
            if res.status_code != 200:
                raise requests.exceptions.HTTPError(
                    f"Error while fetching the privacy odometer, HTTP status code: {res.status_code}, message: {res.text}"
                )
            return json.loads(res.text)

    # Use Oblv Client enclave to make HTTP requests
    def _exec(self, method, endpoint, data="", json={}, params={}, headers={}):
        """
        Execute an HTTP request using the Oblv Client enclave.

        Parameters:
            method (str): The HTTP method.
            endpoint (str): The endpoint URL.
            data (Any, optional): The request data. Defaults to "".
            json (Any, optional): The request JSON. Defaults to None.
            params (dict, optional): The request parameters. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.

        Returns:
            Response: The HTTP response.

        Raises:
            ValueError: If the method is not supported by the client.
        """
        url_endpoint = f"{self.oblv_enclave.url}:{self.oblv_enclave.port}{endpoint}"
        if method == "GET":
            r = self.oblv_enclave.get(
                url_endpoint,
                json=json,
                params=params,
                headers=headers,
            )
        elif method == "POST":
            r = self.oblv_enclave.post(
                url_endpoint, json=json, params=params, headers=headers
            )
        elif method == "PUT":
            r = self.oblv_enclave.put(
                url_endpoint, json=json, params=params, headers=headers
            )
        elif method == "DELETE":
            r = self.oblv_enclave.delete(
                url_endpoint, json=json, params=params, headers=headers
            )
        else:
            raise ValueError(f"{method} not supported by client")
        return r
