class BQBaseError(Exception):
    def __init__(self, status_code, message="Unknown Error Message"):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Error code: {status_code}. {message}")


class BQUnauthorizedError(BQBaseError):
    def __init__(self):
        super().__init__(
            "BQ_ACCESS_UNAUTHORIZED",
            "Wrong API key. You can find your API key once you log in to https://app.bluequbit.io",
        )


class BQStatevectorTooLargeError(BQBaseError):
    def __init__(self, num_qubits):
        super().__init__(
            "BQ_JOB_STATEVECTOR_TOO_LARGE",
            f"Statevector is too large for {num_qubits} qubits. Use .get_counts() instead.",
        )


class BQJobNotCompleteError(BQBaseError):
    def __init__(self, job_id, run_status, error_message):
        super().__init__(
            "BQ_JOB_NOT_COMPLETE",
            f"Job {job_id} finished with status: {run_status}. {error_message}",
        )
        self.job_id = job_id
        self.run_status = run_status
        self.error_message = error_message


class BQJobCouldNotCancelError(BQBaseError):
    def __init__(self, job_id, run_status, error_message):
        super().__init__(
            "BQ_JOB_COULDNOT_CANCEL",
            f"Couldn't cancel job {job_id}. Finished status is {run_status}. {error_message}",
        )
        self.job_id = job_id
        self.run_status = run_status
        self.error_message = error_message
