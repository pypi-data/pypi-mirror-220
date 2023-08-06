from datazone.errors.base import DatazoneError


class DatazoneServiceError(DatazoneError):
    message = "Datazone Service Error"


class DatazoneServiceNotAccessibleError(DatazoneError):
    message = "Datazone Service is not accessible."
