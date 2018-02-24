import sqlite3
import unittest

from src.db.engine import Engine
from src.db.connection import Connection

RESOURCE1 = {'resource_id': 1, 'goal_id': 2,
             'user_id': 1, 'title': 'How to use skies',
             'link': 'https://www.tyrol.com/things-to-do/sports/cross-country-skiing/how-to-get-started',
             'topic': 'sports', 'description': 'Helpful if you are really into skiing',
             'required_time': 12, 'rating': 1}
RESOURCE2 = {'resource_id': 2, 'goal_id': 4,
             'user_id': 2, 'title': 'Cross fit best practices',
             'link': 'https://breakingmuscle.com/fitness/the-formula-for-a-successful-crossfit-gym',
             'topic': 'sports', 'description': 'Key to success in crossfit',
             'required_time': 7, 'rating': 0.9}
RESOURCE3 = {'resource_id': 3, 'goal_id': 1,
             'user_id': 3, 'title': 'US citizenship requirement',
             'link': 'https://www.uscis.gov/us-citizenship/citizenship-through-naturalization',
             'topic': 'life', 'description': 'US is an option, although the healthcare system maybe not as good',
             'required_time': 3, 'rating': 0.9}
RESOURCE4 = {'resource_id': 4, 'goal_id': 5,
             'user_id': 4, 'title': 'Flute techniques',
             'link': 'https://www.vsl.co.at/en/Concert_flute/Playing_Techniques/',
             'topic': 'music', 'description': 'It helped me a lot to learn the basic and advanced techniques',
             'required_time': 40, 'rating': 0.85}
RESOURCE5 = {'resource_id': 5, 'goal_id': 5,
             'user_id': 4, 'title': 'Piano techniques',
             'link': 'https://www.vsl.co.at/en/Concert_piano/Playing_Techniques/',
             'topic': 'music', 'description': 'It helped me a lot to learn the basic and advanced techniques',
             'required_time': 50, 'rating': 0.7}

RESOURCE1_MODIFIED = {'resource_id': 1, 'goal_id': 2,
                      'user_id': 1, 'title': 'How to use skies',
                      'link': 'https://www.tyrol.com/things-to-do/sports/cross-country-skiing/how-to-get-started',
                      'topic': 'sports', 'description': 'Helpful if you are really into skiing',
                      'required_time': 12, 'rating': 0.5}

VALID_RESOURCE_IDS = (1, 2, 3, 4, 5)
VALID_RESOURCES = (RESOURCE1, RESOURCE2, RESOURCE3, RESOURCE4, RESOURCE5)

MALFORMED_ID = 'one'
NON_EXISTING_ID = 100

TEST_DB_PATH = 'db/forum_test.db'
ENGINE = Engine(TEST_DB_PATH)

TEST_GOAL_ID = 5
VALID_RESOURCE_IDS_FOR_TEST_GOAL = (4, 5)
VALID_RESOURCES_FOR_TEST_GOAL = (RESOURCE4, RESOURCE5)
TEST_USER_ID = 4
VALID_RESOURCE_IDS_FOR_TEST_USER = (4, 5)
VALID_RESOURCES_FOR_TEST_USER = (RESOURCE4, RESOURCE5)
TEST_MAX_NUMBER = 3
VALID_RESOURCE_IDS_FOR_TEST_MAX_NUMBER = (1, 2, 3)
VALID_RESOURCES_FOR_TEST_MAX_NUMBER = (RESOURCE1, RESOURCE2, RESOURCE3)
TEST_MAX_TIME = 10
VALID_RESOURCE_IDS_FOR_TEST_MAX_TIME = (2, 3)
VALID_RESOURCES_FOR_TEST_MAX_TIME = (RESOURCE2, RESOURCE3)

NUM_FIELDS_IN_LIST_ITEM = 3


class ResourceDBAPITestCase(unittest.TestCase):

    # INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''

        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''

        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        '''Populates the database'''

        try:
            ENGINE.populate_tables()
            self.connection = ENGINE.connect()
        except Exception as e:
            ENGINE.clear()

    def tearDown(self):
        '''Close underlying connection and remove all records from database'''

        self.connection.close()
        ENGINE.clear()

    def test_get_resource(self):
        '''
        Test get_resource with id 1 and 4
        '''

        print('(' + self.test_get_resource.__name__ + ')',
              self.test_get_resource.__doc__)

        resource = self.connection.get_resource(VALID_RESOURCE_IDS[0])
        self.assertDictContainsSubset(resource, VALID_RESOURCES[0])
        resource = self.connection.get_resource(VALID_RESOURCE_IDS[3])
        self.assertDictContainsSubset(resource, VALID_RESOURCES[3])

    def test_get_resource_malformed_id(self):
        '''
        Test get_resource with id 'one' (malformed)
        '''

        print('(' + self.test_get_resource_malformed_id.__name__ + ')',
              self.test_get_resource_malformed_id.__doc__)

        resource = self.connection.get_resource(MALFORMED_ID)
        self.assertIsNone(resource)

    def test_get_resource_non_existing_id(self):
        '''
        Test get_resource with 10 (no-existing)
        '''

        print('(' + self.test_get_resource_non_existing_id.__name__ + ')',
              self.test_get_resource_non_existing_id.__doc__)

        resource = self.connection.get_resource(NON_EXISTING_ID)
        self.assertIsNone(resource)

    def test_get_resources(self):
        '''
        Test that get_resources_for_goal retrieves all messages
        '''

        print('(' + self.test_get_resources.__name__ + ')',
              self.test_get_resources.__doc__)

        resources = self.connection.get_resources()
        self.assertEqual(len(resources), len(VALID_RESOURCE_IDS))

        for resource in resources:
            self.assertEqual(len(resource), NUM_FIELDS_IN_LIST_ITEM)
            self.assertIn(resource['resource_id'], VALID_RESOURCE_IDS)
            index = VALID_RESOURCE_IDS.index(resource['resource_id'])
            self.assertDictContainsSubset(resource, VALID_RESOURCES[index])

    def test_get_resources_for_goal(self):
        '''
        Test that get_resources retrieves all messages for a goal
        '''

        print('(' + self.test_get_resources_for_goal.__name__ + ')',
              self.test_get_resources_for_goal.__doc__)

        resources = self.connection.get_resources(goal_id=TEST_GOAL_ID)
        self.assertEqual(len(resources), len(VALID_RESOURCES_FOR_TEST_GOAL))

        for resource in resources:
            self.assertEqual(len(resource), NUM_FIELDS_IN_LIST_ITEM)
            self.assertIn(resource['resource_id'], VALID_RESOURCE_IDS_FOR_TEST_GOAL)
            index = VALID_RESOURCE_IDS_FOR_TEST_GOAL.index(resource['resource_id'])
            self.assertDictContainsSubset(resource, VALID_RESOURCES_FOR_TEST_GOAL[index])

    def test_get_resources_for_goal_malformed_id(self):
        '''
        Test get_resources for goal with malformed id
        '''

        print('(' + self.test_get_resources_for_goal_malformed_id.__name__ + ')',
              self.test_get_resources_for_goal_malformed_id.__doc__)

        resources = self.connection.get_resources(goal_id=MALFORMED_ID)
        self.assertIsNone(resources)

    def test_get_resources_for_goal_non_existing_id(self):
        '''
        Test get_resources for non existing goal
        '''

        print('(' + self.test_get_resources_for_goal_non_existing_id.__name__ + ')',
              self.test_get_resources_for_goal_non_existing_id.__doc__)

        resources = self.connection.get_resources(goal_id=NON_EXISTING_ID)
        self.assertEqual(len(resources), 0)

    def test_get_resources_for_user(self):
        '''
        Test that get_resources retrieves all messages for a user
        '''

        print('(' + self.test_get_resources_for_user.__name__ + ')',
              self.test_get_resources_for_user.__doc__)

        resources = self.connection.get_resources(user_id=TEST_USER_ID)
        self.assertEqual(len(resources), len(VALID_RESOURCES_FOR_TEST_USER))

        for resource in resources:
            self.assertEqual(len(resource), NUM_FIELDS_IN_LIST_ITEM)
            self.assertIn(resource['resource_id'], VALID_RESOURCE_IDS_FOR_TEST_USER)
            index = VALID_RESOURCE_IDS_FOR_TEST_USER.index(resource['resource_id'])
            self.assertDictContainsSubset(resource, VALID_RESOURCES_FOR_TEST_USER[index])

    def test_get_resources_for_user_malformed_id(self):
        '''
        Test get_resources for user with malformed id
        '''

        print('(' + self.test_get_resources_for_user_malformed_id.__name__ + ')',
              self.test_get_resources_for_user_malformed_id.__doc__)

        resources = self.connection.get_resources(user_id=MALFORMED_ID)
        self.assertIsNone(resources)

    def test_get_resources_for_user_non_existing_id(self):
        '''
        Test get_resources for non existing user
        '''

        print('(' + self.test_get_resources_for_user_non_existing_id.__name__ + ')',
              self.test_get_resources_for_user_non_existing_id.__doc__)

        resources = self.connection.get_resources(user_id=NON_EXISTING_ID)
        self.assertEqual(len(resources), 0)

    def test_get_resources_limit(self):
        '''
        Test get_resources with a limited maximum number of resources
        '''

        print('(' + self.test_get_resources_limit.__name__ + ')',
              self.test_get_resources_limit.__doc__)

        resources = self.connection.get_resources(number_of_resource=TEST_MAX_NUMBER)
        self.assertEqual(len(resources), len(VALID_RESOURCES_FOR_TEST_MAX_NUMBER))

        for resource in resources:
            self.assertEqual(len(resource), NUM_FIELDS_IN_LIST_ITEM)
            self.assertIn(resource['resource_id'], VALID_RESOURCE_IDS_FOR_TEST_MAX_NUMBER)
            index = VALID_RESOURCE_IDS_FOR_TEST_MAX_NUMBER.index(resource['resource_id'])
            self.assertDictContainsSubset(resource, VALID_RESOURCES_FOR_TEST_MAX_NUMBER[index])

    def test_get_resources_limit_zero(self):
        '''
        Test get_resources with a limit of the maximum number of resources equal to zero
        '''

        print('(' + self.test_get_resources_limit_zero.__name__ + ')',
              self.test_get_resources_limit_zero.__doc__)

        resources = self.connection.get_resources(number_of_resource=0)
        self.assertEqual(len(resources), 0)

    def test_get_resources_limit_non_numerical(self):
        '''
        Test get_resources with a non numerical limit to the maximum number of resources
        '''

        print('(' + self.test_get_resources_limit_non_numerical.__name__ + ')',
              self.test_get_resources_limit_non_numerical.__doc__)

        resources = self.connection.get_resources(number_of_resource='zero')
        self.assertIsNone(resources)

    def test_get_resources_max_duration(self):
        '''
        Test get_resources with a maximum required time
        '''

        print('(' + self.test_get_resources_max_duration.__name__ + ')',
              self.test_get_resources_max_duration.__doc__)

        resources = self.connection.get_resources(max_length=TEST_MAX_TIME)
        self.assertEqual(len(resources), len(VALID_RESOURCES_FOR_TEST_MAX_TIME))

        for resource in resources:
            self.assertEqual(len(resource), NUM_FIELDS_IN_LIST_ITEM)
            self.assertIn(resource['resource_id'], VALID_RESOURCE_IDS_FOR_TEST_MAX_TIME)
            index = VALID_RESOURCE_IDS_FOR_TEST_MAX_TIME.index(resource['resource_id'])
            self.assertDictContainsSubset(resource, VALID_RESOURCES_FOR_TEST_MAX_TIME[index])

    def test_get_resources_max_duration_no_results(self):
        '''
        Test get_resources with a maximum required time set to a low value. No
        results should be found
        '''

        print('(' + self.test_get_resources_max_duration_no_results.__name__ + ')',
              self.test_get_resources_max_duration_no_results.__doc__)

        resources = self.connection.get_resources(max_length=1)
        self.assertEqual(len(resources), 0)

    def test_get_resources_max_duration_negative(self):
        '''
        Test get_resources with a maximum required time set to negative
        '''

        print('(' + self.test_get_resources_max_duration_negative.__name__ + ')',
              self.test_get_resources_max_duration_negative.__doc__)

        resources = self.connection.get_resources(max_length=-50)
        self.assertEqual(len(resources), 0)

    def test_get_resources_max_duration_non_numerical(self):
        '''
        Test get_resources with a maximum required time set to non numerical value
        '''

        print('(' + self.test_get_resources_max_duration_non_numerical.__name__ + ')',
              self.test_get_resources_max_duration_non_numerical.__doc__)

        resources = self.connection.get_resources(max_length='zero')
        self.assertIsNone(resources)

    def test_get_resources_all_filters(self):
        '''
        Test get_resources with all filters used
        '''

        print('(' + self.test_get_resources_all_filters.__name__ + ')',
              self.test_get_resources_all_filters.__doc__)

        resources = self.connection.get_resources(goal_id=TEST_GOAL_ID, user_id=TEST_USER_ID,
                                                  number_of_resource=1, max_length=45)
        self.assertEqual(len(resources), 1)
        resource = resources[0]
        self.assertEqual(len(resource), NUM_FIELDS_IN_LIST_ITEM)
        self.assertDictContainsSubset(resource, VALID_RESOURCES[3])

    def test_delete_resource(self):
        '''
        Test that the resource with id 1 is deleted
        '''

        print('(' + self.test_delete_resource.__name__ + ')',
              self.test_delete_resource.__doc__)

        response = self.connection.delete_resource(RESOURCE1['resource_id'])
        self.assertTrue(response)

        response = self.connection.get_resource(RESOURCE1['resource_id'])
        self.assertIsNone(response)

    def test_delete_resource_malformed_id(self):
        '''
        Test that trying to delete resource with id ='one' fails
        '''
        print('(' + self.test_delete_resource_malformed_id.__name__ + ')',
              self.test_delete_resource_malformed_id.__doc__)

        response = self.connection.delete_resource(MALFORMED_ID)
        self.assertFalse(response)

    def test_delete_resource_non_existing_id(self):
        '''
        Test that trying to delete resource with id ='100' (no-existing) fails
        '''

        print('(' + self.test_delete_resource_non_existing_id.__name__ + ')', \
              self.test_delete_resource_non_existing_id.__doc__)

        response = self.connection.delete_resource(NON_EXISTING_ID)
        self.assertFalse(response)

    def test_modify_resource(self):
        '''
        Test that the resource is modified
        '''

        print('(' + self.test_modify_resource.__name__ + ')',
              self.test_modify_resource.__doc__)

        response = self.connection.modify_resource(RESOURCE1['resource_id'], 0.5)
        self.assertEqual(response, RESOURCE1['resource_id'])

        response = self.connection.get_resource(RESOURCE1['resource_id'])
        self.assertEqual(response, RESOURCE1_MODIFIED)

    def test_modify_message_malformed_id(self):
        '''
        Test that trying to modify resource with id ='one' fails
        '''

        print('(' + self.test_modify_message_malformed_id.__name__ + ')',
              self.test_modify_message_malformed_id.__doc__)

        response = self.connection.modify_resource(MALFORMED_ID, 0.5)
        self.assertIsNone(response)

    def test_modify_message_non_existing_id(self):
        '''
        Test that trying to modify resource with id ='100' (non existing) fails
        '''

        print('(' + self.test_modify_message_non_existing_id.__name__ + ')',
              self.test_modify_message_non_existing_id.__doc__)

        response = self.connection.modify_resource(NON_EXISTING_ID, 0.5)
        self.assertIsNone(response)

    def test_modify_resource_malformed_rating(self):
        '''
        Test that trying to modify resource with rating ='ten' (bad type) fails
        '''

        print('(' + self.test_modify_resource_malformed_rating.__name__ + ')',
              self.test_modify_resource_malformed_rating.__doc__)

        response = self.connection.modify_resource(RESOURCE1['resource_id'], 'ten')
        self.assertIsNone(response)


if __name__ == '__main__':
    print('Start running resource tests')
    unittest.main()
