class InvalideURLException(Exception):
    """This class have excetion of Invalid URL

    Args:
        Exception (InvalidURL): When URL is not valide then exception raised
    """

    def __init__(self, message: str = "Not Valid URL"):
        """
            Initializes the exception with a message.
            This is used to inform the user that the URL is invalid and not a valid one

            @param message - The message to display
        """
        self.message = message
        super().__init__(self.message)
