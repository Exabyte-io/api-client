from endpoints.jobs import ExabyteJobsEndpoint
from tests.integration import EndpointBaseIntegrationTest


class EndpointJobsIntegrationTest(EndpointBaseIntegrationTest):
    """
    Class for testing jobs endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointJobsIntegrationTest, self).__init__(*args, **kwargs)
        self.jobs_endpoint = ExabyteJobsEndpoint(**self.endpoint_kwargs)

    def tearDown(self):
        for job in self.jobs_endpoint.get_jobs():
            self.jobs_endpoint.delete_job(job['_id'])

    def create_job(self, kwargs=None):
        job = self.get_content_in_json('new-job.json')
        job.update(kwargs if kwargs is not None else {})
        return self.jobs_endpoint.create_job(job)

    def test_get_jobs(self):
        job = self.create_job()
        self.assertIn(job['_id'], [m['_id'] for m in self.jobs_endpoint.get_jobs()])

    def test_get_jobs_pagination(self):
        for _ in range(10):
            self.create_job()
        jobs_page_one = self.jobs_endpoint.get_jobs({'pageSize': 5, 'pageIndex': 0})
        jobs_page_two = self.jobs_endpoint.get_jobs({'pageSize': 5, 'pageIndex': 1})
        self.assertEqual(len(jobs_page_one), 5)
        self.assertEqual(len(jobs_page_two), 5)
        self.assertNotEqual([m['_id'] for m in jobs_page_one], [m['_id'] for m in jobs_page_two])

    def test_get_job_by_id(self):
        job = self.create_job()
        self.assertEqual(self.jobs_endpoint.get_job(job['_id'])['_id'], job['_id'])

    def test_create_job(self):
        job = self.create_job()
        self.assertIsNotNone(job['_id'])

    def test_delete_job(self):
        job = self.create_job()
        self.jobs_endpoint.delete_job(job['_id'])
        self.assertNotIn(job['_id'], [m['_id'] for m in self.jobs_endpoint.get_jobs()])

    def test_update_job(self):
        job = self.create_job()
        updated_job = self.jobs_endpoint.update_job(job['_id'], {'tittle': 'NEW TITTLE'})
        self.assertEqual(updated_job['tittle'], 'NEW TITTLE')
