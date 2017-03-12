from endpoints.pseudos import ExabytePseudosEndpoint
from tests.integration import EndpointBaseIntegrationTest


class EndpointPseudosIntegrationTest(EndpointBaseIntegrationTest):
    """
    Class for testing pseudos endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointPseudosIntegrationTest, self).__init__(*args, **kwargs)
        self.pseudos_endpoint = ExabytePseudosEndpoint(**self.endpoint_kwargs)
        self.pseudo = self.pseudos_endpoint.upload_pseudo(self.get_file_path('pseudo'))

    def test_get_pseudos(self):
        self.assertIn(self.pseudo['_id'], [p['_id'] for p in self.pseudos_endpoint.get_pseudos()])

    def test_get_pseudo_by_id(self):
        self.assertEqual(self.pseudos_endpoint.get_pseudo(self.pseudo['_id'])['_id'], self.pseudo['_id'])
