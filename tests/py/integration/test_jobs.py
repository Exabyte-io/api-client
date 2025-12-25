import datetime
import time

from mat3ra.api_client.endpoints.jobs import JobEndpoints
from tests.py.integration.entity import EntityIntegrationTest

KNOWN_COMPLETED_JOB_ID = "9gyhfncWDhnSyzALv"
JOB_NAME_PREFIX = "API-CLIENT TEST JOB"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_NODES = 1
DEFAULT_NOTIFY = "n"
DEFAULT_PPN = 1
DEFAULT_QUEUE = "D"
DEFAULT_TIME_LIMIT = "00:05:00"
TEST_TIME_LIMIT = "00:10:00"
TEST_NOTIFY = "abe"
JOB_STATUS_SUBMITTED = "submitted"
JOB_STATUS_FINISHED = "finished"
JOB_WAIT_TIMEOUT = 900
JOB_WAIT_SLEEP_INTERVAL = 5
JOB_TIMEOUT_ERROR = "job with ID {} did not finish within {} seconds"


class JobEndpointsIntegrationTest(EntityIntegrationTest):
    """
    Job endpoints integration tests.
    """

    def __init__(self, *args, **kwargs):
        super(JobEndpointsIntegrationTest, self).__init__(*args, **kwargs)
        self.endpoints = JobEndpoints(**self.endpoint_kwargs)

    def get_default_config(self):
        """
        Returns the default entity config.
        Override upon inheritance.
        """
        now_time = datetime.datetime.today().strftime(DATETIME_FORMAT)
        return {"name": f"{JOB_NAME_PREFIX} {now_time}"}

    def get_compute_params(self, nodes=DEFAULT_NODES, notify=DEFAULT_NOTIFY, ppn=DEFAULT_PPN, queue=DEFAULT_QUEUE,
                           time_limit=DEFAULT_TIME_LIMIT):
        return {"nodes": nodes, "notify": notify, "ppn": ppn, "queue": queue, "timeLimit": time_limit}

    def test_list_jobs(self):
        self.list_entities_test()

    def test_get_job_by_id(self):
        self.get_entity_by_id_test()

    def test_create_job(self):
        self.create_entity_test()

    def test_delete_job(self):
        self.delete_entity_test()

    def test_update_job(self):
        self.update_entity_test()

    def _wait_for_job_to_finish(self, id_, timeout=JOB_WAIT_TIMEOUT):
        end = time.time() + timeout
        while time.time() < end:
            job = self.endpoints.get(id_)
            if job["status"] == JOB_STATUS_FINISHED:
                return
            time.sleep(JOB_WAIT_SLEEP_INTERVAL)
        raise BaseException(JOB_TIMEOUT_ERROR.format(id_, timeout))

    def test_submit_job_and_wait_to_finish(self):
        job = self.create_entity()
        self.endpoints.submit(job["_id"])
        self.assertEqual(JOB_STATUS_SUBMITTED, self.endpoints.get(job["_id"])["status"])
        self._wait_for_job_to_finish(job["_id"])

    def test_create_job_timeLimit(self):
        job = self.create_entity({"compute": self.get_compute_params(time_limit=TEST_TIME_LIMIT)})
        self.assertEqual(self.endpoints.get(job["_id"])["_id"], job["_id"])
        self.assertEqual(self.endpoints.get(job["_id"])["compute"]["timeLimit"], TEST_TIME_LIMIT)

    def test_create_job_notify(self):
        job = self.create_entity({"compute": self.get_compute_params(notify=TEST_NOTIFY)})
        self.assertEqual(self.endpoints.get(job["_id"])["_id"], job["_id"])
        self.assertEqual(self.endpoints.get(job["_id"])["compute"]["notify"], TEST_NOTIFY)

    def test_list_files(self):
        http_response_data = self.endpoints.list_files(KNOWN_COMPLETED_JOB_ID)
        self.assertIsInstance(http_response_data, list)
        self.assertGreater(len(http_response_data), 0)
        self.assertIsInstance(http_response_data[0], dict)
