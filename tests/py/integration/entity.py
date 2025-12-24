import time

from requests.exceptions import HTTPError

from tests.py.integration import BaseIntegrationTest

INTEGRATION_TEST_TAG = "INTEGRATION-TEST"
ENTITY_ID_KEY = "_id"
ENTITY_NAME_KEY = "name"
ENTITY_TAGS_KEY = "tags"
TEST_NAME_PREFIX = "test-"
UPDATED_NAME = "UPDATED"
WARNING_ENTITY_NOT_FOUND = "WARNING: Entity with ID {} not found in the list of tagged entities: {}"
WARNING_DELETE_FAILED = "WARNING: Failed to delete entity with ID {}: {}"


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
        return {ENTITY_TAGS_KEY: INTEGRATION_TEST_TAG}

    def tearDown(self):
        """Delete only the current test entity if it still exists after test.

        Warn if the filtering fails, failsafe attempt to delete the entity anyways.
        """
        tagged_test_entity_id_list = [e[ENTITY_ID_KEY] for e in self.endpoints.list(query=self.entities_selector())]
        try:
            if self.entity_id not in tagged_test_entity_id_list:
                print(WARNING_ENTITY_NOT_FOUND.format(self.entity_id, tagged_test_entity_id_list))
            self.endpoints.delete(self.entity_id)

        except HTTPError as e:
            print(WARNING_DELETE_FAILED.format(self.entity_id, e))

    def get_default_config(self):
        """
        Returns the default entity config.
        Override upon inheritance.
        """
        raise NotImplementedError

    def create_entity(self, kwargs=None):
        entity = self.get_default_config()
        entity.update(kwargs or {})
        entity.setdefault(ENTITY_TAGS_KEY, []).append(INTEGRATION_TEST_TAG)
        created_entity = self.endpoints.create(entity)
        self.entity_id = created_entity[ENTITY_ID_KEY]
        return created_entity

    def list_entities_test(self):
        entity = self.create_entity()
        self.assertIn(entity[ENTITY_ID_KEY],
                      [e[ENTITY_ID_KEY] for e in self.endpoints.list(query=self.entities_selector())])

    def get_entity_by_id_test(self):
        entity = self.create_entity()
        self.assertEqual(self.endpoints.get(entity[ENTITY_ID_KEY])[ENTITY_ID_KEY], entity[ENTITY_ID_KEY])

    def create_entity_test(self):
        name = f"{TEST_NAME_PREFIX}{time.time()}"
        entity = self.create_entity({ENTITY_NAME_KEY: name})
        self.assertEqual(entity[ENTITY_NAME_KEY], name)
        self.assertIsNotNone(entity[ENTITY_ID_KEY])
        self.assertIn(INTEGRATION_TEST_TAG, entity[ENTITY_TAGS_KEY])

    def delete_entity_test(self):
        entity = self.create_entity()
        self.endpoints.delete(entity[ENTITY_ID_KEY])
        self.assertNotIn(entity[ENTITY_ID_KEY],
                         [e[ENTITY_ID_KEY] for e in self.endpoints.list(query=self.entities_selector())])

    def update_entity_test(self):
        entity = self.create_entity()
        updated_entity = self.endpoints.update(entity[ENTITY_ID_KEY], {ENTITY_NAME_KEY: UPDATED_NAME})
        self.assertEqual(updated_entity[ENTITY_NAME_KEY], UPDATED_NAME)
