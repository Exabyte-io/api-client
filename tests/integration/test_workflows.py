from endpoints.workflows import ExabyteWorkflowsEndpoint
from tests.integration import EndpointBaseIntegrationTest


class EndpointWorkflowsBaseIntegrationTest(EndpointBaseIntegrationTest):
    """
    Class for testing workflows endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointWorkflowsBaseIntegrationTest, self).__init__(*args, **kwargs)
        self.workflows_endpoint = ExabyteWorkflowsEndpoint(**self.endpoint_kwargs)

    def tearDown(self):
        for workflow in [w for w in self.workflows_endpoint.get_workflows() if w['name'] == 'TEST WORKFLOW']:
            self.workflows_endpoint.delete_workflow(workflow['_id'])

    def create_workflow(self, kwargs=None):
        workflow = self.get_content_in_json('workflow.json')
        workflow.update(kwargs if kwargs is not None else {})
        return self.workflows_endpoint.create_workflow(workflow)

    def test_get_workflows(self):
        workflow = self.create_workflow()
        self.assertIn(workflow['_id'], [w['_id'] for w in self.workflows_endpoint.get_workflows()])

    def test_get_workflows_pagination(self):
        for _ in range(10):
            self.create_workflow()
        workflows_page_one = self.workflows_endpoint.get_workflows({'pageSize': 5, 'pageIndex': 0})
        workflows_page_two = self.workflows_endpoint.get_workflows({'pageSize': 5, 'pageIndex': 1})
        self.assertEqual(len(workflows_page_one), 5)
        self.assertEqual(len(workflows_page_two), 5)
        self.assertNotEqual([w['_id'] for w in workflows_page_one], [w['_id'] for w in workflows_page_two])

    def test_get_workflow_by_id(self):
        workflow = self.create_workflow()
        self.assertEqual(self.workflows_endpoint.get_workflow(workflow['_id'])['_id'], workflow['_id'])

    def test_create_workflow(self):
        workflow = self.create_workflow()
        self.assertIsNotNone(workflow['_id'])

    def test_delete_workflow(self):
        workflow = self.create_workflow()
        self.workflows_endpoint.delete_workflow(workflow['_id'])
        self.assertNotIn(workflow['_id'], [w['_id'] for w in self.workflows_endpoint.get_workflows()])

    def test_update_workflow(self):
        workflow = self.create_workflow()
        updated_workflow = self.workflows_endpoint.update_workflow(workflow['_id'], {'name': 'NEW NAME'})
        self.assertEqual(updated_workflow['name'], 'NEW NAME')
        self.workflows_endpoint.delete_workflow(workflow['_id'])
