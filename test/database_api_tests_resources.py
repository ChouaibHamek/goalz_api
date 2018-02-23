import sqlite3
import unittest

from src.db.engine import Engine
from src.db.connection import Connection

RESOURCE1_ID = 1
RESOURCE1 = {'resource_id': 1, 'goal_id': 2,
             'user_id': 1, 'title': 'How to use skies',
             'link': 'https://www.tyrol.com/things-to-do/sports/cross-country-skiing/how-to-get-started',
             'topic': 'sports', 'description': 'Helpful if you are really into skiing',
             'required_time': 12, 'rating': 1}
RESOURCE2_ID = 4
RESOURCE2 = {'resource_id': 4, 'goal_id': 5,
             'user_id': 4, 'title': 'Flute techniques',
             'link': 'https://www.vsl.co.at/en/Concert_flute/Playing_Techniques/',
             'topic': 'music', 'description': 'It helped me a lot to learn the basic and advanced techniques',
             'required_time': 40, 'rating': 0.85}
MALFORMED_ID = 'one'
NON_EXISTING_ID = 10

TEST_DB_PATH = 'db/forum_test.db'
ENGINE = Engine(TEST_DB_PATH)


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

        resource = self.connection.get_resource(RESOURCE1_ID)
        self.assertDictContainsSubset(resource, RESOURCE1)
        resource = self.connection.get_resource(RESOURCE2_ID)
        self.assertDictContainsSubset(resource, RESOURCE2)

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


if __name__ == '__main__':
    print('Start running resource tests')
    unittest.main()
