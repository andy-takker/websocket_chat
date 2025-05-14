class WebsockerChatException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class RepositoryException(WebsockerChatException):
    pass


class UserAlreadyExistsException(RepositoryException):
    pass
