'''
Created on 23.02.2018

Database interface testing for all users related methods.
The user has a dictionary data represented contains:
    {'public_profile':{'registration_date':,'nickname':'','rating':'',
                        'website':''},
     'restricted_profile':{'firstname':'','lastname':'','email':'',
                            'password:'',age':'','gender':''}
    }
    where:

        * ``registration_date``: UNIX timestamp when the user registered in
                                 the system (integer)
        * ``nickname``: nickname of the user (string).
        * ``firstanme``: given name of the user (string).
        * ``lastname``: family name of the user (string).
        * ``email``: current email of the user (string).
        * ``password``: current password of the user (string).
        * ``age``: age of the user (integer).
        * ``gender``: gender of the user. (string).
        * ``rating``: user's rating based on the resource posted (float).
        * ``website``: user's personal web URL (string).

The user data dictionary to modify user contains:
    {'password':'',firstname':'','lastname':'',
    'email':'', 'age':'','gender':'','website':''}

    where:

        * ``password``: new passowrd of the user (string).
        * ``firstanme``: new given name of the user (string).
        * ``lastname``: new family name of the user (string).
        * ``email``: new email of the user (string).
        * ``age``: new age of the user (integer).
        * ``gender``: new gender information of the user (string).
        * ``website``: new user's personal web URL (string).

The user data dictionary to create a new user contains:
    {'firstname':'','lastname':'',
     'email':'', 'password:'','age':'','gender':'',
     'website':''}
List of users and users public data has the data dictionary contains:
    [{'registration_date':'','nickname':'','rating':'','website':''}]

Reference: Code adapted and modified from PWP2018 exercise
'''
import sqlite3, unittest
from src.db import engine
#Path to the database file, different from the deployment db
DB_PATH = 'db/goalz_test.db'
ENGINE = engine.Engine(DB_PATH)

#CONSTANTS DEFINING DIFFERENT USERS AND USER PROPERTIES
USER1_NICKNAME = 'Chouaib'
USER1_ID = 1
USER1 = {'public_profile': {'registration_date': 1362015937,
                            'nickname': USER1_NICKNAME,
                            'rating': 0.9,
                            'website': 'https://github.com/ChouaibHamek'},
         'restricted_profile': {'firstname': 'Chouaib',
                                'lastname': 'Ha',
                                'email': 'c@h.com',
                                'password': 'E6C5F49BD4DF062BC92419C7EA63806B',
                                'age': 24,
                                'gender': 'M'}
         }
MODIFIED_USER1 = {'password':'Y6C5G49BD4DF062CD92419T7EA63806V',
                 'firstname':'Cho',
                 'lastname':'Hamek',
                  'email':'ch@h.com',
                  'age':25,
                  'gender':'M',
                  'website':'https://github.com/ChouaibHamek'}

USER2_NICKNAME = 'Daniel'
USER2_ID = 2
USER2 = {'public_profile': {'registration_date': 1357724086,
                            'nickname': USER2_NICKNAME,
                            'rating': 0.8,
                            'website': 'https://github.com/dtoniuc'},
         'restricted_profile': {'firstname': 'Daniel',
                                'lastname': 'To',
                                'email': 'd@t.com',
                                'password': 'AA47F8215C6F30A0DCDB2A36A9F4168E',
                                'age': 18,
                                'gender': 'M'}
         }
NEW_USER_NICKNAME = 'Nathan'
NEW_USER = {'firstname':'Nathan',
            'lastname':'East',
            'email':'ne@101e.com',
            'password':'E6C5F49BD4DF062BC92419C7EA63806B',
            'age':50,
            'gender':'M',
            'website':'www.nathaneast.com'
            }
NEW_USER_GET = {'public_profile': {'registration_date': 1519490313,
                            'nickname': NEW_USER_NICKNAME,
                            'rating': 0,
                            'website': 'www.nathaneast.com'},
                'restricted_profile': {'firstname': 'Nathan',
                                'lastname': 'East',
                                'email': 'ne@101e.com',
                                'password': 'E6C5F49BD4DF062BC92419C7EA63806B',
                                'age': 50,
                                'gender': 'M'}
                }
USER_WRONG_NICKNAME = 'Angelia'
USER_WRONG_ID = '100'
INITIAL_SIZE = 6

class UserDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.
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
            ENGINE.populate_tables()
            self.connection = ENGINE.connect()
        except Exception as e:
            ENGINE.clear()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()

    def test_users_table_created(self):
        '''
        Checks that the table initially contains 6 users
        '''
        print('('+self.test_users_table_created.__name__+')', \
              self.test_users_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM users'
        query2 = 'SELECT * FROM user_profile'
        #Connects to the database.
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query1)
            users = cur.fetchall()
            #Assert
            self.assertEqual(len(users), INITIAL_SIZE)
            #Check the user_profile:
            cur.execute(query2)
            users = cur.fetchall()
            #Assert
            self.assertEqual(len(users), INITIAL_SIZE)

    def test_create_user_object(self):
        '''
        Check that the method create_user_object works return adequate values
        for the first database row.
        '''
        print('('+self.test_create_user_object.__name__+')', \
              self.test_create_user_object.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT users.*, user_profile.* FROM users, user_profile \
                 WHERE users.user_id = ? \
                 AND user_profile.user_id = users.user_id'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (USER1_ID, )
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
        user = self.connection.user_repo._create_user_object(row)
        self.assertDictContainsSubset(user, USER1)

    def test_get_user_by_id(self):
        '''
        Test get_user with id of Chouaib and Daniel
        '''
        print('('+self.test_get_user_by_id.__name__+')', \
              self.test_get_user_by_id.__doc__)

        #Test with an existing user
        user = self.connection.get_user(USER1_ID)
        self.assertDictContainsSubset(user, USER1)
        user = self.connection.get_user(USER2_ID)
        self.assertDictContainsSubset(user, USER2)

    def test_get_user_by_nickname(self):
        '''
        Test get_user with nickname (Chouaib and Daniel)
        '''
        print('('+self.test_get_user_by_nickname.__name__+')', \
              self.test_get_user_by_nickname.__doc__)

        #Test with an existing user
        user = self.connection.get_user(nickname=USER1_NICKNAME)
        self.assertDictContainsSubset(user, USER1)
        user = self.connection.get_user(nickname=USER2_NICKNAME)
        self.assertDictContainsSubset(user, USER2)

    def test_get_user_public_by_id(self):
        '''
        Test get_user_public with id of Chouaib and Daniel
        '''
        print('('+self.test_get_user_public_by_id.__name__+')', \
              self.test_get_user_public_by_id.__doc__)

        #Test with an existing user
        user = self.connection.get_user_public(USER1_ID)
        self.assertDictContainsSubset(user, USER1['public_profile'])
        user = self.connection.get_user_public(USER2_ID)
        self.assertDictContainsSubset(user, USER2['public_profile'])

    def test_get_user_public_by_nickname(self):
        '''
        Test get_user_public with nickname (Chouaib and Daniel)
        '''
        print('('+self.test_get_user_public_by_nickname.__name__+')', \
              self.test_get_user_public_by_nickname.__doc__)

        #Test with an existing user
        user = self.connection.get_user_public(nickname=USER1_NICKNAME)
        self.assertDictContainsSubset(user, USER1['public_profile'])
        user = self.connection.get_user_public(nickname=USER2_NICKNAME)
        self.assertDictContainsSubset(user, USER2['public_profile'])

    def test_get_user_non_existing_id(self):
        '''
        Test get_user with non existing ID
        '''
        print('('+self.test_get_user_non_existing_id.__name__+')', \
              self.test_get_user_non_existing_id.__doc__)

        #Test with an no existing user
        user = self.connection.get_user(USER_WRONG_ID)
        self.assertIsNone(user)


    def test_get_user_non_existing_nickname(self):
        '''
        Test get_user with non existing nicnkname
        '''
        print('('+self.test_get_user_non_existing_nickname.__name__+')', \
              self.test_get_user_non_existing_nickname.__doc__)

        #Test with an no existing user
        user = self.connection.get_user(USER_WRONG_NICKNAME)
        self.assertIsNone(user)

    def test_get_user_public_non_existing_id(self):
        '''
        Test get_user_public with non existing ID
        '''
        print('('+self.test_get_user_public_non_existing_id.__name__+')', \
              self.test_get_user_public_non_existing_id.__doc__)

        #Test with an no existing user
        user = self.connection.get_user_public(USER_WRONG_ID)
        self.assertIsNone(user)

    def test_get_user_public_non_existing_nickname(self):
        '''
        Test get_user_public with non existing nickname
        '''
        print('('+self.test_get_user_public_non_existing_nickname.__name__+')', \
              self.test_get_user_public_non_existing_nickname.__doc__)

        #Test with an no existing user
        user = self.connection.get_user_public(USER_WRONG_NICKNAME)
        self.assertIsNone(user)

    def test_get_users(self):
        '''
        Test that get_users work correctly and extract required user info
        '''
        print('('+self.test_get_users.__name__+')', \
              self.test_get_users.__doc__)
        users = self.connection.get_users()
        #Check that the size is correct
        self.assertEqual(len(users), INITIAL_SIZE)
        #Iterate throug users and check if the users with USER1_ID and
        #USER2_ID are correct:
        for user in users:
            if user['nickname'] == USER1_NICKNAME:
                self.assertDictContainsSubset(user, USER1['public_profile'])
            elif user['nickname'] == USER2_NICKNAME:
                self.assertDictContainsSubset(user, USER2['public_profile'])

    def test_delete_user(self):
        '''
        Test that the user Chouaib is deleted by id 
        '''
        print('('+self.test_delete_user.__name__+')', \
              self.test_delete_user.__doc__)
        resp = self.connection.delete_user(USER1_ID)
        self.assertTrue(resp)
        #Check that the users has been really deleted throug a get
        resp2 = self.connection.get_user(USER1_ID)
        self.assertIsNone(resp2)

    def test_delete_user_non_existing_id(self):
        '''
        Test delete_user with  USER_WRONG_ID (non-existing)
        '''
        print('('+self.test_delete_user_non_existing_id.__name__+')', \
              self.test_delete_user_non_existing_id.__doc__)
        #Test with an existing user
        resp = self.connection.delete_user(USER_WRONG_ID)
        self.assertFalse(resp)

    def test_modify_user(self):
        '''
        Test that the user Chouaib is modifed
        '''
        print('('+self.test_modify_user.__name__+')', \
              self.test_modify_user.__doc__)
        #Get the modified user
        resp = self.connection.modify_user(USER1_ID, MODIFIED_USER1)
        self.assertEqual(resp, USER1_ID)
        #Check that the users has been really modified through a get
        resp2 = self.connection.get_user(USER1_ID)
        resp_p_profile = resp2['public_profile']
        resp_r_profile = resp2['restricted_profile']
        #Check the expected values
        profile = MODIFIED_USER1
        self.assertEqual(profile['website'],resp_p_profile['website'])
        self.assertEqual(profile['password'], resp_r_profile['password'])
        self.assertEqual(profile['firstname'], resp_r_profile['firstname'])
        self.assertEqual(profile['lastname'], resp_r_profile['lastname'])
        self.assertEqual(profile['email'], resp_r_profile['email'])
        self.assertEqual(profile['age'], resp_r_profile['age'])

    def test_modify_user_noexistingnickname(self):
        '''
        Test modify_user with  user Angelia (no-existing)
        '''
        print('('+self.test_modify_user_noexistingnickname.__name__+')', \
              self.test_modify_user_noexistingnickname.__doc__)
        #Test with an existing user
        resp = self.connection.modify_user(USER_WRONG_ID, MODIFIED_USER1)
        self.assertIsNone(resp)

    def test_create_user(self):
        '''
        Test create a new user
        '''
        print('('+self.test_create_user.__name__+')', \
              self.test_create_user.__doc__)
        nickname = self.connection.create_user(NEW_USER_NICKNAME, NEW_USER)
        self.assertIsNotNone(nickname)
        self.assertEqual(nickname, NEW_USER_NICKNAME)
        #Check that the messages has been really modified through a get
        resp2 = self.connection.get_user(nickname=nickname)
        resp2_r_profile = resp2['restricted_profile']
        resp2_p_profile = resp2['public_profile']
        new_r_profile = NEW_USER_GET['restricted_profile']
        new_p_profile = NEW_USER_GET['public_profile']
        self.assertEqual(new_p_profile['website'],resp2_p_profile['website'])
        self.assertEqual(new_p_profile['rating'],resp2_p_profile['rating'])
        self.assertEqual(new_r_profile['firstname'], resp2_r_profile['firstname'])
        self.assertEqual(new_r_profile['lastname'], resp2_r_profile['lastname'])
        self.assertEqual(new_r_profile['email'], resp2_r_profile['email'])
        self.assertEqual(new_r_profile['password'], resp2_r_profile['password'])
        self.assertEqual(new_r_profile['age'], resp2_r_profile['age'])
        self.assertEqual(new_r_profile['gender'], resp2_r_profile['gender'])

    def test_create_existing_user(self):
        '''
        Test add a new user with an existing nickname
        '''
        print('('+self.test_create_existing_user.__name__+')', \
              self.test_create_existing_user.__doc__)
        nickname = self.connection.create_user(USER1_NICKNAME, NEW_USER)
        self.assertIsNone(nickname)

    def test_get_user_id(self):
        '''
        Test that get_user_id returns the right value given a nickname
        '''
        print('('+self.test_get_user_id.__name__+')', \
              self.test_get_user_id.__doc__)
        id = self.connection.get_user_id(USER1_NICKNAME)
        self.assertEqual(USER1_ID, id)
        id = self.connection.get_user_id(USER2_NICKNAME)
        self.assertEqual(USER2_ID, id)

    def test_get_user_id_unknown_user(self):
        '''
        Test that get_user_id returns None when the nickname does not exist
        '''
        print('('+self.test_get_user_id_unknown_user.__name__+')', \
              self.test_get_user_id_unknown_user.__doc__)
        id = self.connection.get_user_id(USER_WRONG_NICKNAME)
        self.assertIsNone(id)

    def test_not_contains_user(self):
        '''
        Check if the database does not contain users with id Angelia
        '''
        print('('+self.test_contains_user.__name__+')', \
              self.test_contains_user.__doc__)
        self.assertFalse(self.connection.contains_user(USER_WRONG_NICKNAME))

    def test_contains_user(self):
        '''
        Check if the database contains users with nickname Chouaib and Daniel
        '''
        print('('+self.test_contains_user.__name__+')', \
              self.test_contains_user.__doc__)
        self.assertTrue(self.connection.contains_user(USER1_NICKNAME))
        self.assertTrue(self.connection.contains_user(USER2_NICKNAME))

if __name__ == '__main__':
    print('Start running user tests')
    unittest.main()
