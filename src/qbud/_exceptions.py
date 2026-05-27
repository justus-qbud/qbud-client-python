class QBudBaseException(Exception):
    def __init__(self, message):
        super().__init__(message)


class QBudInvalidCredentialsError(QBudBaseException):

    def __init__(self):
        super().__init__(
            "An assistant access key is required. Pass access_key=... to Assistant(), "
            "or set the QBUD_ASSISTANT_ACCESS_KEY environment variable."
        )


class QBudResourceNotFound(QBudBaseException):

    def __init__(self, message):
        default_message = "This resource does not exist."
        super().__init__(message if message else default_message)


class QBudAssistantNotFound(QBudResourceNotFound):

    def __init__(self):
        super().__init__("The assistant ID is invalid, or the access key does not grant access to it.")


class QBudChatNotFound(QBudResourceNotFound):

    def __init__(self):
        super().__init__("The chat ID is invalid.")
