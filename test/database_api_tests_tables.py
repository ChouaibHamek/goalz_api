'''
Created on 23.02.2018
Database interface tests which are testing
correctness of the tables' schemas and correctness of tables' creation

Reference: Code taken and modified from PWP2018 exercise
'''

import sqlite3, unittest

from src.db import engine, connection, constants

#Path to the database file, different from the deployment db
DB_PATH = 'db/goalz_test.db'
ENGINE = engine.Engine(DB_PATH)

INITIAL_USERS_SIZE = 6
INITIAL_GOALS_SIZE = 9
INITIAL_RESOURCES_SIZE = 5

class CreatedTablesTestCase(unittest.TestCase):
    '''
    Test cases for the created tables.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        '''
        Creates the database structure. Removes first any preexisting database file.
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
          #This method loads the initial values from goalz_data_dump.sql
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

    def test_users_table_schema(self):
        '''
        Checks that the USERS table has the right schema.
        '''
        print('('+self.test_users_table_schema.__name__+')', \
                  self.test_users_table_schema.__doc__)

        con = self.connection.con
        with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('users'))

            # Collect names in a list
            result = c.fetchall()
            names = [tup[1] for tup in result]
            types = [tup[2] for tup in result]
            real_names=['user_id','nickname','registration_date','password']
            real_types=['INTEGER','TEXT','INTEGER','TEXT']
            # Check that names and types are correct
            self.assertEqual(names, real_names)    
            self.assertEqual(types, real_types)

    def test_users_table_created(self):
        '''
        Checks that the USERS table initially contains INITIAL_USERS_SIZE number of users (check goalz_data_dump.sql).
        '''
        print('('+self.test_users_table_created.__name__+')', \
                  self.test_users_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users'
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
            users = cur.fetchall()
            #Assert
            self.assertEqual(len(users), INITIAL_USERS_SIZE)

    def test_user_profile_table_schema(self):
        '''
        Checks that the USER_PROFILE table has the right schema.
        '''
        print('(' + self.test_user_profile_table_schema.__name__ + ')', \
              self.test_user_profile_table_schema.__doc__)

        con = self.connection.con
        with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('user_profile'))

            # Collect names in a list
            result = c.fetchall()
            names = [tup[1] for tup in result]
            types = [tup[2] for tup in result]
            real_names = ['user_profile_id', 'user_id', 'firstname', 'lastname', 'email', 'website', 'rating', 'age', 'gender']
            real_types = ['INTEGER', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'REAL', 'INTEGER', 'TEXT']
            # Check that names and types are correct
            self.assertEqual(names, real_names)
            self.assertEqual(types, real_types)

            # Check that foreign keys are correctly set
            foreign_keys = [('users', 'user_id', 'user_id')]
            c.execute('PRAGMA FOREIGN_KEY_LIST({})'.format('user_profile'))
            result = c.fetchall()
            result_filtered = [(tup[2], tup[3],tup[4]) for tup in result]
            for tup in result_filtered:
                self.assertIn(tup, foreign_keys)

    def test_user_profile_table_created(self):
        '''
        Checks that the USER_PROFILE table initially contains INITIAL_USERS_SIZE number of user_profiles (check goalz_data_dump.sql).
        '''
        print('(' + self.test_user_profile_table_created.__name__ + ')', \
              self.test_user_profile_table_created.__doc__)
        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM user_profile'
        # Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            cur.execute(query)
            user_profiles = cur.fetchall()
            # Assert
            self.assertEqual(len(user_profiles), INITIAL_USERS_SIZE)

    def test_goals_table_schema(self):
        '''
        Checks that the GOALS table has the right schema.
        '''
        print('(' + self.test_goals_table_schema.__name__ + ')', \
              self.test_goals_table_schema.__doc__)

        con = self.connection.con
        with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('goals'))

            # Collect names in a list
            result = c.fetchall()
            names = [tup[1] for tup in result]
            types = [tup[2] for tup in result]
            real_names = ['goal_id', 'parent_id', 'user_id', 'title', 'topic', 'description', 'deadline', 'status']
            real_types = ['INTEGER', 'INTEGER', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER']
            # Check that names and types are correct
            self.assertEqual(names, real_names)
            self.assertEqual(types, real_types)

            # Check that foreign keys are correctly set
            foreign_keys = [('goals', 'parent_id', 'goal_id'),
                            ('users', 'user_id', 'user_id')]
            c.execute('PRAGMA FOREIGN_KEY_LIST({})'.format('goals'))
            result = c.fetchall()
            result_filtered = [(tup[2], tup[3], tup[4]) for tup in result]
            for tup in result_filtered:
                self.assertIn(tup, foreign_keys)

    def test_goals_table_created(self):
        '''
        Checks that the GOALS table initially contains INITIAL_GOALS_SIZE number of goals (check goalz_data_dump.sql).
        '''
        print('(' + self.test_goals_table_created.__name__ + ')', \
              self.test_goals_table_created.__doc__)
        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM goals'
        # Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            cur.execute(query)
            goals = cur.fetchall()
            # Assert
            self.assertEqual(len(goals), INITIAL_GOALS_SIZE)

    def test_resources_table_schema(self):
        '''
        Checks that the RESOURCES table has the right schema.
        '''
        print('(' + self.test_resources_table_schema.__name__ + ')', \
              self.test_resources_table_schema.__doc__)

        con = self.connection.con
        with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('resources'))

            # Collect names in a list
            result = c.fetchall()
            names = [tup[1] for tup in result]
            types = [tup[2] for tup in result]
            real_names = ['resource_id', 'goal_id', 'user_id', 'title', 'link', 'topic', 'description', 'required_time', 'rating']
            real_types = ['INTEGER', 'INTEGER', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'INTEGER', 'REAL']
            # Check that names and types are correct
            self.assertEqual(names, real_names)
            self.assertEqual(types, real_types)

            # Check that foreign keys are correctly set
            foreign_keys = [('goals', 'goal_id', 'goal_id'),
                            ('users', 'user_id', 'user_id')]
            c.execute('PRAGMA FOREIGN_KEY_LIST({})'.format('resources'))
            result = c.fetchall()
            result_filtered = [(tup[2], tup[3], tup[4]) for tup in result]
            for tup in result_filtered:
                self.assertIn(tup, foreign_keys)

    def test_resources_table_created(self):
        '''
        Checks that the RESOURCES table initially contains INITIAL_RESOURCES_SIZE number of resources (check goalz_data_dump.sql).
        '''
        print('(' + self.test_goals_table_created.__name__ + ')', \
              self.test_goals_table_created.__doc__)
        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM resources'
        # Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            cur.execute(query)
            resources = cur.fetchall()
            # Assert
            self.assertEqual(len(resources), INITIAL_RESOURCES_SIZE)

    def test_foreign_keys_status(self):
        '''
        Checks that the foreign keys support is set and unset correctly.
        '''
        print('(' + self.test_foreign_keys_status.__name__ + ')', \
              self.test_foreign_keys_status.__doc__)
        # Checks that foreign key support is activated
        success = self.connection.set_foreign_keys_support()
        if success:
            fk_status = self.connection.check_foreign_keys_status()
            self.assertTrue(fk_status)

        # Checks that foreign key support is deactivated
        success = self.connection.unset_foreign_keys_support()
        if success:
            fk_status = self.connection.check_foreign_keys_status()
            self.assertFalse(fk_status)

if __name__ == '__main__':
    print('Start running database tests')
    unittest.main()
