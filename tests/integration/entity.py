import time

from requests.exceptions import HTTPError

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
        """Delete only the current test entity if it still exists after test.

        Warn if the filtering fails, failsafe attempt to delete the entity anyways.
        """
        tagged_test_entity_id_list = [e["_id"] for e in self.endpoints.list(query=self.entities_selector())]
        try:
            if self.entity_id not in tagged_test_entity_id_list:
                print(
                    f"WARNING: Entity with ID {self.entity_id} not found in the list of tagged entities:"
                    f" {tagged_test_entity_id_list}"
                )
            self.endpoints.delete(self.entity_id)

        except HTTPError as e:
            print(f"WARNING: Failed to delete entity with ID {self.entity_id}: {e}")

    def get_default_config(self):
        """
        Returns the default entity config.
        Override upon inheritance.
        """
        raise NotImplementedError

    def create_entity(self, kwargs=None):
        entity = self.get_default_config()
        entity.update(kwargs or {})
        entity.setdefault("tags", []).append("INTEGRATION-TEST")
        created_entity = self.endpoints.create(entity)
        self.entity_id = created_entity["_id"]
        return created_entity

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
        self.assertIn("INTEGRATION-TEST", entity["tags"])

    def delete_entity_test(self):
        entity = self.create_entity()
        self.endpoints.delete(entity["_id"])
        self.assertNotIn(entity["_id"], [e["_id"] for e in self.endpoints.list(query=self.entities_selector())])

    def update_entity_test(self):
        entity = self.create_entity()
        updated_entity = self.endpoints.update(entity["_id"], {"name": "UPDATED"})
        self.assertEqual(updated_entity["name"], "UPDATED")
