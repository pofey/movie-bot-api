class MovieBotApiException(Exception):
    pass


class NetworkErrorException(MovieBotApiException):
    pass


class ApiErrorException(MovieBotApiException):
    pass


class IllegalAuthorization(ApiErrorException):
    pass
