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

    def test_goals_table_created(self):
        '''
        Checks that the table initially contains 9 goals
        '''
        print('('+self.test_goals_table_created.__name__+')', \
                  self.test_goals_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM goals'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            goals = cur.fetchall()
            #Assert
            self.assertEqual(len(goals), INITIAL_SIZE)

    def test_create_goal_object(self):
        '''
        Check that the method _create_goal_object works return adequate
        values for the first database row.
        '''
        print('('+self.test_create_goal_object.__name__+')', \
              self.test_create_goal_object.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM goals WHERE goal_id = %s' % str(GOAL1_ID)
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            #Extrac the row
            row = cur.fetchone()
        #Test the method
        goal = self.connection.goal_repo._create_goal_object(row)
        self.assertDictContainsSubset(goal, GOAL1)

    def test_get_goal(self):
        '''
        Test get_goal with id 1 and 2
        '''
        print('('+self.test_get_goal.__name__+')', \
              self.test_get_goal.__doc__)
        #Test with an existing goal
        goal = self.connection.get_goal(GOAL1_ID)
        self.assertDictContainsSubset(goal, GOAL1)
        goal = self.connection.get_goal(GOAL2_ID)
        self.assertDictContainsSubset(goal, GOAL2)


    def test_get_goal_noexistingid(self):
        '''
        Test get_goal with id 30 (no-existing)
        '''
        print('('+self.test_get_goal_noexistingid.__name__+')',\
              self.test_get_goal_noexistingid.__doc__)
        #Test with an existing goal
        goal = self.connection.get_goal(WRONG_GOAL_ID)
        self.assertIsNone(goal)

    def test_get_goals(self):
        '''
        Test that get_goals works correctly
        '''
        print('('+self.test_get_goals.__name__+')', self.test_get_goals.__doc__)
        goals = self.connection.get_goals()
        #Check that the size is correct
        self.assertEqual(len(goals), INITIAL_SIZE)
        #Iterate throug goals and check if the goals with GOAL1_ID and
        #GOAL2_ID are correct:
        for goal in goals:
            if goal['goal_id'] == GOAL1_ID:
                self.assertEqual(len(goal), 4)
                self.assertDictContainsSubset(goal, GOAL1)
            elif goal['goal_id'] == GOAL2_ID:
                self.assertEqual(len(goal), 4)
                self.assertDictContainsSubset(goal, GOAL2)

    def test_get_goals_malformedBefore(self):
        '''
        Test that providing an invalid `before` argument  raises an error
        '''
        print('('+self.test_get_goals_malformedBefore.__name__+')', \
              self.test_get_goals_malformedBefore.__doc__)
        #Test with an existing goal
        with self.assertRaises(ValueError):
            self.connection.get_goals(1, before="not A timestamp")

    def test_get_goals_malformedAfter(self):
        '''
        Test that providing an invalid `after` argument raises an error
        '''
        print('('+self.test_get_goals_malformedAfter.__name__+')', \
              self.test_get_goals_malformedAfter.__doc__)
        #Test with an existing goal
        with self.assertRaises(ValueError):
            self.connection.get_goals(1, after=-1)

    def test_get_goals_specific_user(self):
        '''
        Get all goals from user_id 2. Check that their ids are 2 and 3.
        '''
        #goals related to user_id = 2 are goal_id = 2 and goal_id = 3
        print('('+self.test_get_goals_specific_user.__name__+')', \
              self.test_get_goals_specific_user.__doc__)
        goals = self.connection.get_goals(user_id = 2)
        self.assertEqual(len(goals), 2)
        #goals id are 2 and 3
        for goal in goals:
            self.assertIn(goal['goal_id'], (2, 3))
            self.assertNotIn(goal['goal_id'], (1, 4, 5, 6, 7, 8, 9))

    def test_get_goals_length(self):
        '''
        Check that the number_of_goals is working in get_goals
        '''
        #goals related to user_id = 2 are 2
        print('('+self.test_get_goals_length.__name__+')',\
              self.test_get_goals_length.__doc__)
        goals = self.connection.get_goals(user_id = 2,
                                                number_of_goals=2)
        self.assertEqual(len(goals), 2)
        goals = self.connection.get_goals(number_of_goals=1)
        self.assertEqual(len(goals), 1)


    def test_delete_goal(self):
        '''
        Test that the goal 1 is deleted
        '''
        print('('+self.test_delete_goal.__name__+')', \
              self.test_delete_goal.__doc__)
        resp = self.connection.delete_goal(GOAL1_ID)
        self.assertTrue(resp)
        #Check that the goals has been really deleted throug a get
        resp2 = self.connection.get_goal(GOAL1_ID)
        self.assertIsNone(resp2)


    def test_delete_goal_noexistingid(self):
        '''
        Test delete_goal with  30 (no-existing)
        '''
        print('('+self.test_delete_goal_noexistingid.__name__+')', \
              self.test_delete_goal_noexistingid.__doc__)
        #Test with an existing goal
        resp = self.connection.delete_goal(WRONG_GOAL_ID)
        self.assertFalse(resp)

    def test_modify_goal(self):
        '''
        Test that the goal 1 is modifed
        '''
        print('('+self.test_modify_goal.__name__+')', \
              self.test_modify_goal.__doc__)
        resp = self.connection.modify_goal(GOAL1_ID, 'Done',
                'Accomplished Lifed and Travel', 'Acquired citizenship',
                1740099600, 1.0)
        self.assertEqual(resp, GOAL1_ID)
        #Check that the goals has been really modified through a get
        resp2 = self.connection.get_goal(GOAL1_ID)
        self.assertDictContainsSubset(resp2, GOAL1_MODIFIED)

    def test_modify_goal_singleField(self):
        '''
        Test that only the status of goal 1 is updated
        '''
        print('('+self.test_modify_goal.__name__+')', \
              self.test_modify_goal.__doc__)
        resp = self.connection.modify_goal(GOAL1_ID, status=0.98)
        self.assertEqual(resp, GOAL1_ID)
        #Check that the goals has been really modified through a get
        resp2 = self.connection.get_goal(GOAL1_ID)
        self.assertDictContainsSubset(resp2, GOAL1_STATUS_UPDATED)

    def test_modify_goal_noexistingid(self):
        '''
        Test modify_goal with  30 (no-existing)
        '''
        print('('+self.test_modify_goal_noexistingid.__name__+')',\
              self.test_modify_goal_noexistingid.__doc__)
        #Test with an existing goal
        resp = self.connection.modify_goal(WRONG_GOAL_ID, 'Done',
                'Accomplished Lifed and Travel', 'Acquired citizenship',
                1740099600, 1.0)
        self.assertIsNone(resp)

    def test_create_goal(self):
        '''
        Test that a new goal can be created
        '''
        print('('+self.test_create_goal.__name__+')',\
              self.test_create_goal.__doc__)
        goal_id = self.connection.create_goal(1, "new year, new goal",
                "new topic", "This is described as a new goal")
        self.assertIsNotNone(goal_id)
        #Get the expected modified goal
        new_goal = {}
        new_goal['user_id'] = 1
        new_goal['title'] = "new year, new goal"
        new_goal['topic'] = "new topic"
        new_goal['description'] = "This is described as a new goal"
        #Check that the goal has been really created through a get
        resp2 = self.connection.get_goal(goal_id)
        self.assertDictContainsSubset(new_goal, resp2)
        #CHECK NOW WITH PARENT_ID AND DEADLINE
        goal_id = self.connection.create_goal(1, "new year, new goal",
                "new topic", "This is described as a new goal", 9,
                1534291200)
        self.assertIsNotNone(goal_id)
        #Get the expected modified goal
        new_goal = {}
        new_goal['user_id'] = 1
        new_goal['title'] = "new year, new goal"
        new_goal['topic'] = "new topic"
        new_goal['description'] = "This is described as a new goal"
        new_goal['parent_id'] = 9
        new_goal['deadline'] = 1534291200
        #Check that the goals has been really created through a get
        resp2 = self.connection.get_goal(goal_id)
        self.assertDictContainsSubset(new_goal, resp2)



    def test_not_contains_goal(self):
        '''
        Check if the database does not contain goals with id 30

        '''
        print('('+self.test_contains_goal.__name__+')', \
              self.test_contains_goal.__doc__)
        self.assertFalse(self.connection.contains_goal(WRONG_GOAL_ID))

    def test_contains_goal(self):
        '''
        Check if the database contains goals with id 1 and 2

        '''
        print('('+self.test_contains_goal.__name__+')', \
              self.test_contains_goal.__doc__)
        self.assertTrue(self.connection.contains_goal(GOAL1_ID))
        self.assertTrue(self.connection.contains_goal(GOAL2_ID))

if __name__ == '__main__':
    print('Start running goal tests')
    unittest.main()
