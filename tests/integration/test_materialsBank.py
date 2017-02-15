from endpoints.materialsBank import ExabyteMaterialsBankEndpoint
from tests.integration.test_materials import EndpointMaterialsBaseIntegrationTest


class EndpointMaterialsBankIntegrationTest(EndpointMaterialsBaseIntegrationTest):
    """
    Class for testing materials-bank endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointMaterialsBankIntegrationTest, self).__init__(*args, **kwargs)
        self.materials_bank_endpoint = ExabyteMaterialsBankEndpoint(**self.endpoint_kwargs)

    def test_get_materials(self):
        material = self.create_material()
        self.assertIn(material['exabyteId'], [m['_id'] for m in self.materials_bank_endpoint.get_materials()])
