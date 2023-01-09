from werkzeug.exceptions import HTTPException
from flask import make_response

class UserNotFound(HTTPException):
    def __init__(self, status_code=None):
        self.status_code = status_code
        self.response = make_response('', self.status_code)

class UserExists(HTTPException):
    def __init__(self, status_code=None, errorin=None):
        self.response = make_response(errorin, status_code)

class incorrect_login(HTTPException):
    def __init__(self, status_code=None, errorin=None):
        self.response = make_response(errorin, status_code)

class request_not_allowed(HTTPException):
    def __init__(self, messasge=None, status_code=None):
        self.response = make_response(messasge, status_code)