from datazone.core.connections.auth import AuthService
from os import environ as env

from datazone.errors.common import DatazoneServiceError, DatazoneServiceNotAccessibleError

AUTH_DISABLED = env.get("AUTH_DISABLED", "false") == "true"

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException


class CustomHTTPAdapter(HTTPAdapter):
    def send(self, request, **kwargs):
        try:
            response = super().send(request, **kwargs)
            response.raise_for_status()
            return response
        except RequestException as e:
            if e.response is not None:
                error = e.response.json()
                if error is not None:
                    raise DatazoneServiceError(error)
            raise DatazoneServiceNotAccessibleError


adapter = CustomHTTPAdapter()


def get_session():
    if AUTH_DISABLED:
        session = requests.Session()
    else:
        auth = AuthService()
        session = auth.get_session()

    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
