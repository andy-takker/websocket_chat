class WebsockerChatException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class RepositoryException(WebsockerChatException):
    pass


class UserAlreadyExistsException(RepositoryException):
    pass


class IncorrectCredentialsException(RepositoryException):
    pass


class RefreshTokenNotFoundException(WebsockerChatException):
    pass


class ObjectNotFoundException(RepositoryException):
    pass


class ForbiddenException(WebsockerChatException):
    pass
