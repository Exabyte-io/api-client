import time

from requests import HTTPError

from endpoints.jobs import ExabyteJobsEndpoint
from endpoints.materials import ExabyteMaterialsEndpoint
from endpoints.workflows import ExabyteWorkflowsEndpoint
from tests.integration import EndpointBaseIntegrationTest


class EndpointJobsIntegrationTest(EndpointBaseIntegrationTest):
    """
    Class for testing jobs endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointJobsIntegrationTest, self).__init__(*args, **kwargs)
        self.jobs_endpoint = ExabyteJobsEndpoint(**self.endpoint_kwargs)
        self.materials_endpoint = ExabyteMaterialsEndpoint(**self.endpoint_kwargs)
        self.workflows_endpoint = ExabyteWorkflowsEndpoint(**self.endpoint_kwargs)
        self.material = self.materials_endpoint.create_material(self.get_content_in_json('material.json'))
        self.workflow = self.materials_endpoint.create_material(self.get_content_in_json('workflow.json'))

    def tearDown(self):
        for job in [j for j in self.jobs_endpoint.get_jobs() if j['status'] != 'submitted']:
            self.jobs_endpoint.delete_job(job['_id'])

    def create_job(self, kwargs=None):
        job = self.get_content_in_json('job.json')
        job.update(kwargs if kwargs is not None else {})
        job['_material']['_id'] = self.material['_id']
        job['model']['method']['workflow']['_id'] = self.workflow['_id']
        return self.jobs_endpoint.create_job(job)

    def get_compute_params(self, nodes=1, notify='n', ppn=1, queue='D', time_limit='00:05:00'):
        return {
            "cluster": {"fqdn": "master-vagrant-cluster-001.exabyte.io"},
            "nodes": nodes,
            "notify": notify,
            "ppn": ppn,
            "queue": queue,
            "timeLimit": time_limit
        }

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
        title = "job-{}".format(time.time())
        job = self.create_job({"title": title})
        self.assertEqual(job['title'], title)
        self.assertIsNotNone(job['_id'])

    def test_create_job_d_queue_with_2_nodes(self):
        with self.assertRaises(HTTPError):
            self.create_job({"compute": self.get_compute_params(nodes=2)})

    def test_create_job_timeLimit(self):
        time_limit = "00:10:00"
        job = self.create_job({"compute": self.get_compute_params(time_limit=time_limit)})
        self.assertEqual(self.jobs_endpoint.get_job(job['_id'])['_id'], job['_id'])
        self.assertEqual(self.jobs_endpoint.get_job(job['_id'])['compute']['timeLimit'], time_limit)

    def test_create_job_notify(self):
        job = self.create_job({"compute": self.get_compute_params(notify='abe')})
        self.assertEqual(self.jobs_endpoint.get_job(job['_id'])['_id'], job['_id'])
        self.assertEqual(self.jobs_endpoint.get_job(job['_id'])['compute']['notify'], 'abe')

    def test_delete_job(self):
        job = self.create_job()
        self.jobs_endpoint.delete_job(job['_id'])
        self.assertNotIn(job['_id'], [m['_id'] for m in self.jobs_endpoint.get_jobs()])

    def test_update_job(self):
        job = self.create_job()
        updated_job = self.jobs_endpoint.update_job(job['_id'], {'title': 'NEW TITTLE'})
        self.assertEqual(updated_job['title'], 'NEW TITTLE')

    def test_submit_job(self):
        job = self.create_job()
        self.jobs_endpoint.submit_job(job['_id'])
        self.assertEqual('submitted', self.jobs_endpoint.get_job(job['_id'])['status'])
