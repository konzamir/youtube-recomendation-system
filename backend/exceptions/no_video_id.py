from rest_framework import exceptions, status


class NoVideoIdException(exceptions.APIException):

    def __init__(self, detail=None):
        super().__init__(detail, status.HTTP_403_FORBIDDEN)

        self.status_code = status.HTTP_403_FORBIDDEN
