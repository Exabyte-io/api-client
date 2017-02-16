from endpoints.materials import ExabyteMaterialsEndpoint
from tests.integration import EndpointBaseIntegrationTest


class EndpointMaterialsBaseIntegrationTest(EndpointBaseIntegrationTest):
    """
    Base class for testing materials endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointMaterialsBaseIntegrationTest, self).__init__(*args, **kwargs)
        self.materials_endpoint = ExabyteMaterialsEndpoint(**self.endpoint_kwargs)

    def tearDown(self):
        for material in self.materials_endpoint.get_materials():
            self.materials_endpoint.delete_material(material['_id'])

    def create_material(self, kwargs=None):
        material = self.get_content_in_json('new-material.json')
        material.update(kwargs if kwargs is not None else {})
        return self.materials_endpoint.create_material(material)


class EndpointMaterialsIntegrationTest(EndpointMaterialsBaseIntegrationTest):
    """
    Class for testing materials endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointMaterialsIntegrationTest, self).__init__(*args, **kwargs)

    def test_get_materials(self):
        material = self.create_material()
        self.assertIn(material['_id'], [m['_id'] for m in self.materials_endpoint.get_materials()])

    def test_get_materials_pagination(self):
        for _ in range(10):
            self.create_material()
        materials_page_one = self.materials_endpoint.get_materials({'pageSize': 5, 'pageIndex': 0})
        materials_page_two = self.materials_endpoint.get_materials({'pageSize': 5, 'pageIndex': 1})
        self.assertEqual(len(materials_page_one), 5)
        self.assertEqual(len(materials_page_two), 5)
        self.assertNotEqual([m['_id'] for m in materials_page_one], [m['_id'] for m in materials_page_two])

    def test_get_material_by_id(self):
        material = self.create_material()
        self.assertEqual(self.materials_endpoint.get_material(material['_id'])['_id'], material['_id'])

    def test_get_material_by_id_with_characteristics(self):
        material = self.create_material()
        response = self.materials_endpoint.get_material(material['_id'], {'includeCharacteristics': True})
        self.assertEqual(response['_id'], material['_id'])
        self.assertIsNotNone(response.get('characteristics'))

    def test_get_material_by_formula(self):
        material = self.create_material()
        self.assertIn(material['_id'], [m['_id'] for m in self.materials_endpoint.get_materials_by_formula('Si')])

    def test_create_material(self):
        material = self.create_material()
        self.assertIsNotNone(material['_id'])

    def test_delete_material(self):
        material = self.create_material()
        self.materials_endpoint.delete_material(material['_id'])
        self.assertNotIn(material['_id'], [m['_id'] for m in self.materials_endpoint.get_materials()])

    def test_update_material(self):
        material = self.create_material()
        updated_material = self.materials_endpoint.update_material(material['_id'], {'name': 'NEW NAME'})
        self.assertEqual(updated_material['name'], 'NEW NAME')
