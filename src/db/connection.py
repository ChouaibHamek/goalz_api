'''
Created on 20.02.2018

Provides the database API to access the goal tracker's persistent data.

Reference: Code taken an modified from PWP2018 exercise
'''

import sqlite3

import src.db.constants as constants
from src.db.user_repo import UserRepo

class Connection(object):
    '''
    API to access the Goalz database.

    The sqlite3 connection instance is accessible to all the methods of this
    class through the :py:attr:`self.con` attribute.

    An instance of this class should not be instantiated directly using the
    constructor. Instead use the :py:meth:`Engine.connect`.

    Use the method :py:meth:`close` in order to close a connection.
    A :py:class:`Connection` **MUST** always be closed once when it is not going to be
    utilized anymore in order to release internal locks.

    :param db_path: Location of the database file.
    :type db_path: str
    '''

    def __init__(self, db_path):
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)
        self._isclosed = False
        self.user_repo = UserRepo(self.con)

    def isclosed(self):
        '''
        :return: ``True`` if connection has already being closed.
        '''

        return self._isclosed

    def close(self):
        '''
        Closes the database connection, committing all changes.
        '''

        if self.con and not self._isclosed:
            self.con.commit()
            self.con.close()
            self._isclosed = True

    def check_foreign_keys_status(self):
        '''
        Check if the foreign keys has been activated.

        :return: ``True`` if  foreign_keys is activated and ``False`` otherwise.
        :raises sqlite3.Error: when a sqlite3 error happen. In this case the
            connection is closed.
        '''

        try:
            cur = self.con.cursor()
            cur.execute('PRAGMA foreign_keys')
            data = cur.fetchone()
            is_activated = data == (1,)
            print("Foreign Keys status: %s" % 'ON' if is_activated else 'OFF')
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            self.close()
            raise excp

        return is_activated

    def set_foreign_keys_support(self):
        '''
        Activate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.
        '''

        keys_on = constants.SQL_TURN_FOREIGN_KEY_ON
        try:
            cur = self.con.cursor()
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    def unset_foreign_keys_support(self):
        '''
        Deactivate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.
        '''

        keys_on = constants.SQL_TURN_FOREIGN_KEY_OFF
        try:
            cur = self.con.cursor()
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    # TODO: Implement user methods
    # USER METHODS
    # this methods represent the db api. A description should be provided and the
    # execution should be delegated to a separate class which deals with user
    # db management (can be an inner class)

    def get_user(self, user_id):
        '''
        Extracts all the information of a user.

        :param integer user_id: The unique id of the user to search for.
        :return: dictionary with the format provided in the method:
            :py:meth:`_create_user_object`. None is returned if the database
            has no users with given user_id.
        '''
        self.set_foreign_keys_support()
        return self.user_repo.get_user(user_id)

    def get_user_public(self, nickname):
        '''
        Extracts public information of a user.

        :param string nickname: The nickname of the user to search for.
        :return: user data dictionary with the format provided in the method:
            :py:meth:`_create_user_list_object`. None is returned if the database
            has no users with given nickname.
        '''
        self.set_foreign_keys_support()
        return self.user_repo.get_user_public(nickname)

    def get_users(self):
        '''
        Extracts all users in the database.

        :return: list of Users of the database. Each user is a dictionary
            with the format provided in the method:
            :py:meth:`_create_user_list_object`.
            None is returned if the database has no users.
        '''
        self.set_foreign_keys_support()
        return self.user_repo.get_users()

    def delete_user(self, user_id):
        '''
        Remove all information of the user with the user_id passed in as
        argument.

        :param integer user_id: The unique ID of the user to remove.
        :return: True if the user is deleted, False otherwise.

        '''
        self.set_foreign_keys_support()
        return self.user_repo.delete_user(user_id)

    def modify_user(self, user_id, r_profile):
        '''
        Modify the information of a user.

        :param int user_id: The unique ID of the user to modify
        :param dict r_profile: a dictionary with the restricted information + website(public)
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
        self.set_foreign_keys_support()
        return self.user_repo.modify_user(user_id, r_profile)

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
        self.set_foreign_keys_support()
        return self.user_repo.create_user(nickname, new_user)

    def get_user_id(self, nickname):
        '''
        Get the user_id of the user with the given
        nickname.

        :param str nickname: The nickname of the user to search.
        :return: the database attribute user_id or None if ``nickname`` does
            not exist in the database.
        '''
        self.set_foreign_keys_support()
        return self.user_repo.get_user_id(nickname)

    def contains_user(self, nickname):
        '''
        :return: True if the user is in the database. False otherwise
        '''
        self.set_foreign_keys_support()
        return self.user_repo.get_user_id(nickname)

    # TODO: Implement goals methods
    # GOAL METHODS
    # this methods represent the db api. A description should be provided and the
    # execution should be delegated to a separate class which deals with goals
    # db management (can be an inner class)
    #
    # new methods should be added if required
    def get_goal(self, user):
        raise NotImplementedError("")

    def get_goals(self, user_id=None):
        raise NotImplementedError("")

    def delete_goal(self, user_id):
        raise NotImplementedError("")

    def modify_goal(self):
        # NOTE: this method should have more parameters (check exercises)
        raise NotImplementedError("")

    def create_goal(self):
        # NOTE: this method should have more parameters (check exercises)
        raise NotImplementedError("")

    # HELPERS FOR GOALS
    # this methods should be in a separate class which deals with user db management (can be an inner class)
    def _create_goal_object(self, row):
        # Transforms db row to python dictionary
        raise NotImplementedError("")

    def _create_goal_list_object(self, row):
        # Transforms db row to python dictionary
        raise NotImplementedError("")

    # TODO: Implement resource methods
    # RESOURCE METHODS
    # this methods represent the db api. A description should be provided and the
    # execution should be delegated to a separate class which deals with resources
    # db management (can be an inner class)
    #
    # new methods should be added if required
    def get_resource(self, user):
        raise NotImplementedError("")

    def get_resources(self, user_id=None):
        raise NotImplementedError("")

    def delete_resource(self, user_id):
        raise NotImplementedError("")

    def modify_resource(self):
        # NOTE: this method should have more parameters (check exercises)
        # NOTE: the resource cannot be modified, only their rating
        raise NotImplementedError("")

    def create_resource(self):
        # NOTE: this method should have more parameters (check exercises)
        raise NotImplementedError("")

    # HELPERS FOR GOALS
    # this methods should be in a separate class which deals with user db management (can be an inner class)
    def _create_resource_object(self, row):
        # Transforms db row to python dictionary
        raise NotImplementedError("")

    def _create_resource_list_object(self, row):
        # Transforms db row to python dictionary
        raise NotImplementedError("")
