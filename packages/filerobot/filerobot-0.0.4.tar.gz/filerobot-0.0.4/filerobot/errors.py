


class WrongCredentialsError(Exception):
    """
    Exception raised for errors in case of wrong:
    : filerobot_token
    : filerobot_key

    Attributes:
        request -- input request 404
        message -- explanation of the error
    """
    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)



class FolderNotFoundError(Exception):
    """Exception raised for errors in case of wrong list folder.

        Attributes:
            request -- input request 404
            message -- explanation of the error
    """
    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)


class FileNotFoundError(Exception):
    """Exception raised for errors in case of not found file.

            Attributes:
                request -- input request 404
                message -- explanation of the error
        """

    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)


class UrlContentError(Exception):
    """Exception raised for errors in case of url doesn't contain Content-Lenght header

               Attributes:
                   request -- input request 400
                   message -- explanation of the error
    """

    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)

class FileNameExistError(Exception):
    """Exception raised for errors in case of trying to rename the file with the same name

                   Attributes:
                       request -- input request 409
                       message -- explanation of the error
        """

    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)

class FolderExistsError(Exception):
    """Exception raised for errors in case of trying to create folder that already exist.

                       Attributes:
                           request -- input request 403
                           message -- explanation of the error
    """

    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)


class ParameterTypeError(Exception):
    """
    Exception raised for error in case of tying to parse the parameter in proper format

    """
    def __int__(self, message):
        self.message = message
        super().__init__(self.message)