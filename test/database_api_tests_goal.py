'''
Created on 23.02.2018
Database interface testing for all goals related methods.

A Goal object is a dictionary which contains the following keys:
      - goal_id: id of the goal (int)
      - parent_id: id if of the parent goal (int)
      - user_id: id of the user who created the goal (int)
      - title: goal's title
      - topic: goal's topic
      - description: goal's description
      - deadline: goal's deadline (int)
      - status: goal's completion status (int)

A goals' list has the following format:
[{'goal_id':, 'title':'', 'topic':'', 'description':''},
 {'goal_id':, 'title':'', 'topic':'', 'description':''}]

Reference: Code adapted and modified from PWP2018 exercise
'''

import sqlite3, unittest
from src.db import engine

#Path to the database file, different from the deployment db
DB_PATH = 'db/goalz_test.db'
ENGINE = engine.Engine(DB_PATH)


#CONSTANTS DEFINING DIFFERENT USERS AND USER PROPERTIES
GOAL1_ID = 1

GOAL1 = {'goal_id': 1,
            'parent_id': None,
            'user_id': 1,
            'title': "Acquire citizenship",
            'topic': 'Life, travel',
            'description': 'You know',
            'deadline': 1519172121, 'status': 0.7}

GOAL1_MODIFIED = {'goal_id': 1,
            'parent_id': None,
            'user_id': 1,
            'title': 'Done',
            'topic': 'Accomplished Lifed and Travel',
            'description': 'Acquired citizenship',
            'deadline': 1740099600, 'status': 1.0}

GOAL1_STATUS_UPDATED = {'goal_id': 1,
            'parent_id': None,
            'user_id': 1,
            'title': "Acquire citizenship",
            'topic': 'Life, travel',
            'description': 'You know',
            'deadline': 1519172121, 'status': 0.98}
GOAL2_ID = 2

GOAL2 = {'goal_id': 2,
            'parent_id': None,
            'user_id': 2,
            'title': "Cross country ski",
            'topic': 'sports',
            'description': 'You know',
            'deadline': 1616199840, 'status': 0.1}

WRONG_GOAL_ID = 30

INITIAL_SIZE = 9


class GoalDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the Goals related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
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
        '''
        Populates the database
        '''
        try:
          #This method load the initial values from goalz_data_dump.sql
          ENGINE.populate_tables()
          #Creates a Connection instance to use the API
          self.connection = ENGINE.connect()
        except Exception as e:
        #For instance if there is an error while populating the tables
          ENGINE.clear()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()

if __name__ == '__main__':
    print('Start running goal tests')
    unittest.main()
