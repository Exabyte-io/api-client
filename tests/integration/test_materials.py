from endpoints.materials import ExabyteMaterialsEndpoint
from tests.integration import EndpointBaseIntegrationTest


class EndpointMaterialsIntegrationTest(EndpointBaseIntegrationTest):
    """
    Class for testing materials endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointMaterialsIntegrationTest, self).__init__(*args, **kwargs)
        self.materials_endpoint = ExabyteMaterialsEndpoint(**self.endpoint_kwargs)

    def test_get_materials(self):
        material = self.__create_material()
        materials = self.materials_endpoint.get_materials()
        print materials
        self.assertIn(material['_id'], [m['_id'] for m in materials])

    def test_get_material_by_id(self):
        material = self.__create_material()
        response = self.materials_endpoint.get_material(material['_id'])
        self.assertEqual(response['_id'], material['_id'])

    def test_get_material_by_formula(self):
        material = self.__create_material()
        materials = self.materials_endpoint.get_materials_by_formula('Si')
        self.assertIn(material['_id'], [m['_id'] for m in materials])

    def test_create_material(self):
        material = self.__create_material()
        self.assertIsNotNone(material['_id'])

    def test_delete_material(self):
        material = self.__create_material()
        self.materials_endpoint.delete_material(material['_id'])
        materials = self.materials_endpoint.get_materials()
        self.assertNotIn(material['_id'], [m['_id'] for m in materials])

    def test_update_material(self):
        material = self.__create_material()
        updated_material = self.materials_endpoint.update_material(material['_id'], {'name': 'NEW NAME'})
        self.assertEqual(updated_material['name'], 'NEW NAME')

    def __create_material(self, kwargs=None):
        material = self.get_content_in_json('new-material.json')
        material.update(kwargs if kwargs is not None else {})
        return self.materials_endpoint.create_material(material)
