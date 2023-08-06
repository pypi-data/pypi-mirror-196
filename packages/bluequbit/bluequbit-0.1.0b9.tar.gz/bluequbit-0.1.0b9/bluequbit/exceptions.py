class BQBaseError(Exception):
    def __init__(
        self, status_code="Unknown Status Code", message="Unknown Error Message"
    ):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)


class BQUnauthorizedError(BQBaseError):
    def __init__(self):
        super().__init__(
            401,
            "Wrong API key. You can find your API key once you log in to https://app.bluequbit.io",
        )


class BQStatevectorTooLargeError(BQBaseError):
    def __init__(self, num_qubits):
        super().__init__(
            0,
            f"Statevector is too large for {num_qubits} qubits. Use .get_counts() instead.",
        )


class BQJobNotCompleteError(BQBaseError):
    def __init__(self, job_id, run_status):
        super().__init__(
            1,
            f"Job {job_id} didn't complete with results. Finished status is {run_status}.",
        )
        self.job_id = job_id
        self.run_status = run_status


class BQJobCouldNotCancelError(BQBaseError):
    def __init__(self, job_id, run_status):
        super().__init__(
            2,
            f"Couldn't cancel job {job_id}. Finished status is {run_status}.",
        )
        self.job_id = job_id
        self.run_status = run_status
