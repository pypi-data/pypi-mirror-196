import sys
import inspect
from typing import Optional, Type

from .base import BaseAMOREQQException
from ..amoreqq_api import AIProcessorResponseBody

__all__ = [
    "BaseAMOREQQApiException", "InvalidAMOREQQApiResponseException", "IllegalPictureAMOREQQApiResponseException",
    "get_exception_from_response_code",
]


class BaseAMOREQQApiException(BaseAMOREQQException):
    response_body: str
    response_body_parsed: Optional[AIProcessorResponseBody]

    def __init__(self, msg, response_body, response_body_parsed):
        super().__init__(msg)
        self.response_body = response_body
        self.response_body_parsed = response_body_parsed


class InvalidAMOREQQApiResponseException(BaseAMOREQQApiException):
    error_msg: str = "Invalid response body"
    response_code: Optional[int] = None

    def __init__(self, response_body, response_body_parsed):
        super().__init__(
            msg=self.error_msg,
            response_body=response_body,
            response_body_parsed=response_body_parsed,
        )


class IllegalPictureAMOREQQApiResponseException(InvalidAMOREQQApiResponseException):
    error_msg = "Illegal picture"
    response_code = 2114


class VolumnLimitQQDDMApiResponseException(InvalidAMOREQQApiResponseException):
    error_msg = "API rate limited or picture too big"
    response_code = 2111


class AuthFailedQQDDMApiResponseException(InvalidAMOREQQApiResponseException):
    error_msg = "Auth failed (the API may have changed and the library is currently not compatible)"
    response_code = -2111


class NotAllowedCountryQQDDMApiResponseException(InvalidAMOREQQApiResponseException):
    error_msg = "The current country is blocked by the API"
    response_code = 2119


class NoFaceInPictureQQDDMApiResponseException(InvalidAMOREQQApiResponseException):
    error_msg = "The picture does not have a valid face"
    response_code = 1001


class ParamInvalidAMOREQQApiResponseException(InvalidAMOREQQApiResponseException):
    error_msg = "A request param is invalid or the given picture has an invalid format"
    response_code = -2100


def get_exception_from_response_code(code: int) -> Type[InvalidAMOREQQApiResponseException]:
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if isinstance(obj, type) and issubclass(obj, InvalidAMOREQQApiResponseException) and obj.response_code == code:
            return obj
    return InvalidAMOREQQApiResponseException
