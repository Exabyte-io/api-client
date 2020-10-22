from exabyte_api_client.endpoints.materials import MaterialEndpoints
from tests.integration.entity import EntityIntegrationTest


class MaterialEndpointsIntegrationTest(EntityIntegrationTest):
    """
    Material endpoints integration tests.
    """

    def __init__(self, *args, **kwargs):
        super(MaterialEndpointsIntegrationTest, self).__init__(*args, **kwargs)
        self.endpoints = MaterialEndpoints(**self.endpoint_kwargs)

    def get_default_config(self):
        return self.get_content_in_json('material.json')

    def test_list_materials(self):
        self.list_entities_test()

    def test_get_material_by_id(self):
        self.get_entity_by_id_test()

    def test_create_material(self):
        self.create_entity_test()

    def test_delete_material(self):
        self.delete_entity_test()

    def test_update_material(self):
        self.update_entity_test()

    def test_get_material_by_formula(self):
        material = self.create_entity()
        materials = self.endpoints.list(query={"_id": material["_id"], "formula": 'Si'})
        self.assertIn(material['_id'], [m['_id'] for m in materials])
