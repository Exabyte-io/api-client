import time

from tests.integration import BaseIntegrationTest


class EntityIntegrationTest(BaseIntegrationTest):
    """
    Base entity integration tests class.
    """

    def __init__(self, *args, **kwargs):
        super(EntityIntegrationTest, self).__init__(*args, **kwargs)
        self.endpoints = None
        self.entity_id: str = ""

    def entities_selector(self):
        """
        Returns a selector to access entities created in tests.
        Override upon inheritance as necessary.
        """
        return {"tags": "INTEGRATION-TEST"}

    def tearDown(self):
        [print(e["_id"]) for e in self.endpoints.list(query=self.entities_selector())]
        # for entity in [e for e in self.endpoints.list(query=self.entities_selector())]:
        self.endpoints.delete(self.entity_id)

    def get_default_config(self):
        """
        Returns the default entity config.
        Override upon inheritance.
        """
        raise NotImplementedError

    def create_entity(self, kwargs=None):
        entity = self.get_default_config()
        entity.update(kwargs or {})
        entity["tags"] = entity.get("tags", [])
        entity["tags"].append("INTEGRATION-TEST")
        self.entity_id = entity["_id"]
        return self.endpoints.create(entity)

    def list_entities_test(self):
        entity = self.create_entity()
        self.assertIn(entity["_id"], [e["_id"] for e in self.endpoints.list(query=self.entities_selector())])

    def get_entity_by_id_test(self):
        entity = self.create_entity()
        self.assertEqual(self.endpoints.get(entity["_id"])["_id"], entity["_id"])

    def create_entity_test(self):
        name = "test-{}".format(time.time())
        entity = self.create_entity({"name": name})
        self.assertEqual(entity["name"], name)
        self.assertIsNotNone(entity["_id"])

    def delete_entity_test(self):
        entity = self.create_entity()
        print(self.entity_id)
        self.endpoints.delete(entity["_id"])
        print(f"DELETED: {entity['_id']}")
        self.assertNotIn(entity["_id"], [e["_id"] for e in self.endpoints.list(query=self.entities_selector())])

    def update_entity_test(self):
        entity = self.create_entity()
        updated_entity = self.endpoints.update(entity["_id"], {"name": "UPDATED"})
        self.assertEqual(updated_entity["name"], "UPDATED")
