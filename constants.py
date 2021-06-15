# constants.py
from enum import Enum


class Constants():
    """
    Application Constants.
    """
    BASE_URL = "{0}{1}"
    ENDPOINT = "/wsapis/v2.0.0"
    ACTION_RESULT = "result"
    ACTION_STATUS = "execution_status"
    RESPONSE = "action_response"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    STATUS_CODE = "status_code"


class Auth():
    AUTH_ENDPOINT = '/auth/login'
    AUTH_RESPONSE = "auth_response"
    AUTH_FAIL = "WRONG USERNAME OR PASSWORD"
    AUTH_SUCCESS = "AUTHENTICATION SUCCESSFUL"


class TestConnect():
    CONNECTION_FAILED = "CONNECTION FAILED"
    CONNECTION_SUCCESS = "CONNECTION SUCCESSFUL"
    CONNECTION_FAIL_URL = "URL IS INVALID OR CONNECTION_FAILED OR URL IS NOT WHITELISTED OR NOT ACCESSIBLE"
    MESSAGE = "message"


class CommonEndpoints():
    ALERT = "alerts"
    ARTIFACT = "artifacts"
    CONFIG = "config"
    EVENTS = "events"
    REPORTS = "reports"


class ErrorMsg():
    """
    Connector Error Messages.
    """

    SERVER_ERROR = "Server Error, try again"
    WRONG_MET = "Invalid Requested Method!"


class HTTPRequestTypes(Enum):
    """
    HTTP Request Methods:
    GET     - The GET method is used to retrieve information from the given server using a given URI.
    POST    - A POST request is used to send data to the server using HTML forms.
    """
    GET = "GET"
    POST = "POST"
