
'''
Created on 23.02.2018

Provides the database API to access the goal tracker's persistent data.

Reference: Code adapted and modified from PWP2018 exercise
'''
from datetime import datetime
import src.db.constants as constants
import time, sqlite3

class UserRepo(object):

    def __init__(self, con):
        super(UserRepo, self).__init__()
        self.con = con

    def get_user_public(self, user_id, nickname):
        '''
        Extracts public information of a user by the user_id or nickname
        
        :param integer user_id: The unique ID of the user, default None.
        :param string nickname: The nickname of the user to search for, default None.
        :return: dictionary with the format provided in the method:
            :py:meth:`_create_user_list_object`. None is returned if the database
            has no users with given nickname.

        '''
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        if nickname is not None:
            #Fetch and return user if it exists else return None
            #SQL Statement for retrieving the user given a nickname
            query1 = constants.SQL_SELECT_USER_BY_NICKNAME
            #Execute SQL Statement to retrieve the id given a nickname
            pvalue = (nickname,)
            cur.execute(query1, pvalue)
            #Extract the user id
            row = cur.fetchone()
            if row is None:
                return None
            user_id = row["user_id"]
        elif user_id is None:
            return None
        #Create the SQL Statements
        #SQL Statement for retrieving the user given a user_id
        query = constants.SQL_SELET_USER_AND_PROFILE_BY_ID
        # Execute the SQL Statement to retrieve the user information.
        # Create first the valuse
        pvalue = (user_id, )
        #execute the statement
        cur.execute(query, pvalue)
        #Process the response. Only one posible row is expected.
        row = cur.fetchone()
        if row is None:
            return None
        #return user dictionary
        return self._create_user_list_object(row)


    def get_user(self, user_id, nickname):
        '''
        Extracts all the information of a user by user_id or nickname.

        :param integer user_id: The unique id of the user to search for, default None.
        :param string nickname: The nickname of the user to search for, default None.
        :return: dictionary with the format provided in the method:
            :py:meth:`_create_user_object`. None is returned if the database
            has no users with given user_id.

        '''
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        if nickname is not None:
            #Fetch and return user if it exists else return None
            #SQL Statement for retrieving the user given a nickname
            query1 = constants.SQL_SELECT_USER_BY_NICKNAME
            #Execute SQL Statement to retrieve the id given a nickname
            pvalue = (nickname,)
            cur.execute(query1, pvalue)
            #Extract the user id
            row = cur.fetchone()
            if row is None:
                return None
            user_id = row["user_id"]
        elif user_id is None:
            return None
        #Create the SQL Statements
        #SQL Statement for retrieving the user given a user_id
        query = constants.SQL_SELET_USER_AND_PROFILE_BY_ID
        # Execute the SQL Statement to retrieve the user information.
        # Create first the valuse
        pvalue = (user_id, )
        #execute the statement
        cur.execute(query, pvalue)
        #Process the response. Only one posible row is expected.
        row = cur.fetchone()
        if row is None:
            return None
        #return user dictionary
        return self._create_user_object(row)

    def get_users(self):
        '''
        Extracts all users in the database.

        :return: list of Users of the database. Each user is a dictionary
            with the format provided in the method:
            :py:meth:`_create_user_list_object`.
            None is returned if the database has no users.

        '''
        #Create the SQL Statements
          #SQL Statement for retrieving the users
        query = constants.SQL_SELECT_USER_AND_PROFILE
        #Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Process the results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Process the response.
        users = []
        for row in rows:
            users.append(self._create_user_list_object(row))
        return users


    def delete_user(self, user_id):
        '''
        Remove all information of the user with the user_id passed in as
        argument.

        :param integer user_id: The unique ID of the user to remove.
        :return: True if the user is deleted, False otherwise.

        '''
        #Create the SQL Statements
        #SQL Statement for deleting the user information
        query = constants.SQL_DELETE_USER
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to delete
        pvalue = (user_id,)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that it has been deleted
        if cur.rowcount < 1:
            return False
        else:
            return True


    def modify_user(self, user_id, r_profile):
        '''
        Modify the information of a user.

        :param int user_id: The unique ID of the user to modify
        :param dict r_profile: a dictionary with the restricted informtion + website(public)
                to be modified. The dictionary has the following structure:

                .. code-block:: javascript

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

        :return: the user_id of the modified user or None if the
            ``user_id`` passed is not in the database.

        '''
        #Create the SQL Statements to check if the users exist
        query1 = constants.SQL_SELECT_USER_BY_ID
        #Create the SQL Statements for updating users data
        query2 = constants.SQL_UPDATE_USER_PASSWORD
        #Create the SQL Statements for updating users_profile data
        query3 = constants.SQL_UPDATE_USER_PROFILE
        #temporal variables
        _password = None if not r_profile else r_profile.get('password', None)
        _firstname = None if not r_profile else r_profile.get('firstname', None)
        _lastname = None if not r_profile else r_profile.get('lastname', None)
        _email = None if not r_profile else r_profile.get('email', None)
        _age = None if not r_profile else r_profile.get('age', None)
        _gender = None if not r_profile else r_profile.get('gender', None)
        _website = None if not r_profile else r_profile.get('website', None)

        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #execute the first statement
        pvalue = (user_id, )
        cur.execute(query1, pvalue)
        rows = cur.fetchall()
        if rows is None:
            return None
        else:
            #execute the second statement
            pvalue = (_password, user_id)
            cur.execute(query2, pvalue)
            row1 = cur.rowcount
            #execute the third statement
            pvalue = (_firstname, _lastname, _email, _age, _gender,
                     _website, user_id)

            cur.execute(query3, pvalue)
            self.con.commit()
            row2 = cur.rowcount
            #Check that the password or the user profile have been successfully modified
            if row1 < 1 and row2 < 1:
                return None
            else:
                return user_id


    def create_user(self, nickname, new_user):
        '''
        Create a new user in the database.

        :param  str nickname: The nickname of the user to modify
        :param dict user: a dictionary with the new user information. The
                dictionary has the following structure:

                .. code-block:: javascript

                    {'firstname':'','lastname':'',
                     'email':'', 'password:'','age':'','gender':'',
                     'website':''}

                where:

                * ``firstname``: given name of the user (string).
                * ``lastname``: family name of the user (string).
                * ``email``: email of the user (string).
                * ``password``: given password of the user (string).
                * ``age``: user's age (integer).
                * ``gender``: user's gender. Can be None (string).
                * ``webiste``: user's personal web URL. Can be None (string).

        :return: the nickname of the modified user or None if the
            ``nickname`` passed as parameter is already in the database.

        '''
        #Create the SQL Statements
        #SQL Statement for extracting the userid given a nickname
        query1 = constants.SQL_SELECT_USER_BY_NICKNAME
        #SQL Statement to create the row in  users table
        query2 = constants.SQL_INSERT_USER
        #SQL Statement to create the row in user_profile table
        query3 = constants.SQL_INSERT_USER_PROFILE
        #temporal variables for user table
        #get the current time for registration_date.
        _registration_date = time.mktime(datetime.now().timetuple())
        #temporal variables for user profiles
        #user = new_user['new_profile']
        _firstname = new_user.get('firstname', None)
        _lastname = new_user.get('lastname', None)
        _email = new_user.get('email', None)
        _password = new_user.get('password', None)
        _age = new_user.get('age', None)
        _gender = new_user.get('gender', None)
        _website = new_user.get('website', None)
        _rating = 0
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the main SQL statement to extract the id associated to a nickname
        pvalue = (nickname,)
        cur.execute(query1, pvalue)
        row = cur.fetchone()
        #If there is no nickname with the same value as argument passed, add rows in user and user profile
        if row is None:
            #Add the row in users table
            # Execute the statement
            pvalue = (nickname, _password, _registration_date)
            cur.execute(query2, pvalue)
            #Extrat the rowid => user-id
            lid = cur.lastrowid
            #Add the row in users_profile table
            # Execute the statement
            pvalue = (lid, _firstname, _lastname, _email, _age,
                      _gender, _rating, _website)
            cur.execute(query3, pvalue)
            self.con.commit()
            #return the nickname
            return nickname
        else:
            return None

    def get_user_id(self, nickname):
        '''
        Get the user_id of the user with the given
        nickname.

        :param str nickname: The nickname of the user to search.
        :return: the database attribute user_id or None if ``nickname`` does
            not exist in the database.

        '''
        query = constants.SQL_SELECT_USER_BY_NICKNAME
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the  main SQL statement
        pvalue = (nickname,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        else:
            return row[0]

    def contains_user(self, nickname):
        '''
        :return: True if the user is in the database. False otherwise
        '''
        return self.get_user_id(nickname) is not None

    #Helpers for users
    def _create_user_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the following format:

            .. code-block:: javascript

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

        '''
        regDate = row['registration_date']
        user_object = {'public_profile':{'registration_date':regDate,
                                            'nickname': row['nickname'],
                                            'rating': row['rating'],
                                            'website': row['website']},
                'restricted_profile': {'firstname': row['firstname'],
                                       'lastname': row['lastname'],
                                       'email': row['email'],
                                       'password': row['password'],
                                       'age': row['age'],
                                       'gender': row['gender']}
                }
        return user_object

    #Helpers for users
    def _create_user_list_object(self, row):
        '''
        Same as :py:meth:`_create_user_object`. but, the resulting
        dictionary is targeted to build user list with public data only.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the follwing format:
             .. code-block:: javascript

                {'registration_date':'','nickname':'','rating':'',website:''}

            where:

                * ``registration_date``: UNIX timestamp when the user registered in
                                     the system (integer)
                * ``nickname``: nickname of the user (string).
                * ``rating``: user's rating based on the resource posted (double).
                * ``website``: user's personal web URL (string).

        '''
        user_list_object = {'registration_date': row['registration_date'], 'nickname': row['nickname'],
                            'rating': row['rating'], 'website': row['website']}
        return user_list_object
