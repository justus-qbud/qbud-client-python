class QBudBaseException(Exception):
    def __init__(self, message):
        super().__init__(message)


class QBudAuthenticationError(QBudBaseException):

    def __init__(self, message=None):
        default_message = "The provided client_id and client secret are invalid."
        super().__init__(message if message else default_message)


class QBudInvalidCredentialsError(QBudBaseException):

    def __init__(self):
        super().__init__("You need to set 'QBUD_CLIENT_ID' and 'QBUD_CLIENT_SECRET' environment variables.")


class QbudResourceNotFound(QBudBaseException):

    def __init__(self, message):
        default_message = "This resource does not exist."
        super().__init__(message if message else default_message)


class QBudAssistantNotFound(QbudResourceNotFound):

    def __init__(self):
        super().__init__("The assistant ID is invalid.")


class QbudChatNotFound(QbudResourceNotFound):

    def __init__(self):
        super().__init__("The chat ID is invalid.")
