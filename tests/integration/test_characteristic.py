from endpoints.characteristic import ExabyteCharacteristicEndpoint
from tests.integration import EndpointBaseIntegrationTest


class EndpointCharacteristicIntegrationTest(EndpointBaseIntegrationTest):
    """
    Class for testing characteristic endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointCharacteristicIntegrationTest, self).__init__(*args, **kwargs)
        self.char_endpoint = ExabyteCharacteristicEndpoint(**self.endpoint_kwargs)

    def tearDown(self):
        for char in self.char_endpoint.get_characteristics():
            self.char_endpoint.delete_characteristic(char['_id'])

    def create_characteristic(self, kwargs=None):
        characteristic = self.get_content_in_json('new-characteristic.json')
        characteristic.update(kwargs if kwargs is not None else {})
        return self.char_endpoint.create_characteristic(characteristic)

    def test_get_characteristics(self):
        characteristic = self.create_characteristic()
        self.assertIn(characteristic['_id'], [c['_id'] for c in self.char_endpoint.get_characteristics()])

    def test_get_characteristics_pagination(self):
        for _ in range(10):
            self.create_characteristic()
        characteristics_page_one = self.char_endpoint.get_characteristics({'pageSize': 5, 'pageIndex': 0})
        characteristics_page_two = self.char_endpoint.get_characteristics({'pageSize': 5, 'pageIndex': 1})
        self.assertEqual(len(characteristics_page_one), 5)
        self.assertEqual(len(characteristics_page_two), 5)
        self.assertNotEqual([c['_id'] for c in characteristics_page_one], [c['_id'] for c in characteristics_page_two])

    def test_get_characteristic_by_id(self):
        characteristic = self.create_characteristic()
        self.assertEqual(self.char_endpoint.get_characteristic(characteristic['_id'])['_id'], characteristic['_id'])

    def test_create_characteristic(self):
        characteristic = self.create_characteristic()
        self.assertIsNotNone(characteristic['_id'])

    def test_delete_characteristic(self):
        characteristic = self.create_characteristic()
        self.char_endpoint.delete_characteristic(characteristic['_id'])
        self.assertNotIn(characteristic['_id'], [m['_id'] for m in self.char_endpoint.get_characteristics()])

    def test_update_characteristic(self):
        characteristic = self.create_characteristic()
        updated_characteristic = self.char_endpoint.update_characteristic(characteristic['_id'], {'name': 'NEW NAME'})
        self.assertEqual(updated_characteristic['name'], 'NEW NAME')
