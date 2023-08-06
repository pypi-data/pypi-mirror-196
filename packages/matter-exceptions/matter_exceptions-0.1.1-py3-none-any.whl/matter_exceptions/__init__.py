__all__ = ["BaseAPIException", "DetailedException", "AuthenticationFailedError"]

from http.client import HTTPException


class BaseAPIException(HTTPException):
    def __init__(self, description, payload: dict | None = None, type: str | None = None):
        super().__init__(description)

        self.data = {}
        if payload:
            self.data.update(payload)

        self.data["type"] = type
        self.data["message"] = description
        self.data["success"] = False


class DetailedException(Exception):
    TOPIC = "Error"

    def __init__(self, message: str, data=None):
        self.message = message if self.TOPIC in message else f"{self.TOPIC}: {message}"
        self.data = data
        self.type = self.TOPIC.replace(" ", "_").lower()

    def __reduce__(self):
        return self.__class__, (
            self.message,
            self.data,
        )

    def __eq__(self, other):
        return other.__reduce__() == self.__reduce__()


class AuthenticationFailedError(DetailedException):
    TOPIC = "Authentication Failed Error"
