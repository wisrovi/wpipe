from wpipe.log import new_logger

logger = new_logger()


class Codes:
    UPDATE_TASK = 505
    UPDATE_PROCESS_ERROR = 504
    UPDATE_PROCESS_OK = 503
    TASK_FAILED = 502
    API_ERROR = 501


class ApiError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

        logger.error(message)


class TaskError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

        logger.error(message)


class ProcessError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

        logger.error(message)
