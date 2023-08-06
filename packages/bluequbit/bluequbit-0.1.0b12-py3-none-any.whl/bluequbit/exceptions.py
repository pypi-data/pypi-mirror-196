from . import job_metadata_constants


class BQError(Exception):
    def __init__(self, message="Unknown Error Message"):
        super().__init__(message)
        self.message = message


class BQUnauthorizedAccessError(BQError):
    def __init__(self):
        super().__init__(
            "Wrong API key. You can find your API key once you log in to https://app.bluequbit.io."
        )


class BQStatevectorTooLargeError(BQError):
    def __init__(self, num_qubits):
        super().__init__(
            f"Statevector is too large for {num_qubits} qubits. Use .get_counts() instead.",
        )


class BQJobNotCompleteError(BQError):
    def __init__(self, job_id, run_status, error_message):
        super().__init__(
            f"Job {job_id} finished with status: {run_status}. {error_message}",
        )
        self.job_id = job_id
        self.run_status = run_status
        self.error_message = error_message


class BQJobCouldNotCancelError(BQError):
    def __init__(self, job_id, run_status, error_message):
        super().__init__(
            f"Couldn't cancel job {job_id}. Finished status is {run_status}. {error_message}",
        )
        self.job_id = job_id
        self.run_status = run_status


class BQAPIError(BQError):
    def __init__(self, http_status_code, error_message):
        super().__init__(
            f"{error_message}. HTTP response status code: {http_status_code}.",
        )
        self.http_status_code = http_status_code
        self.error_message = error_message


class BQInvalidDeviceTypeError(BQError):
    def __init__(self, device):
        super().__init__(
            f"Invalid device type {device}. Must be one of {', '.join(job_metadata_constants.DEVICE_TYPES)}."
        )
