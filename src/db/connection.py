'''
Created on 20.02.2018

Provides the database API to access the goal tracker's persistent data.

Reference: Code taken an modified from PWP2018 exercise
'''

import sqlite3
from src.db import constants
from src.db.resource_repo import ResourceRepo


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
        self.resource_repo = ResourceRepo(self.con)

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
    #
    # new methods should be added if required
    def get_user(self, user):
        raise NotImplementedError("")

    def get_user(self, user_id):
        raise NotImplementedError("")

    def get_users(self):
        raise NotImplementedError("")

    def delete_user(self, user_id):
        raise NotImplementedError("")

    def modify_user(self):
        # NOTE: this method should have more parameters (check exercises)
        raise NotImplementedError("")

    def create_user(self):
        # NOTE: this method should have more parameters (check exercises)
        raise NotImplementedError("")

    # HELPERS FOR USERS
    # this methods should be in a separate class which deals with user db management (can be an inner class)
    def _create_user_object(self, row):
        # Transforms db row to python dictionary
        raise NotImplementedError("")

    def _create_user_list_object(self, row):
        # Transforms db row to python dictionary
        raise NotImplementedError("")

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

    # RESOURCE METHODS
    def get_resource(self, resource_id):
        self.set_foreign_keys_support()
        return self.resource_repo.get_resource(resource_id)

    def get_resources(self, goal_id=None, user_id=None,
                      number_of_resource=None, max_length=None):
        self.set_foreign_keys_support()
        return self.resource_repo.get_resources(goal_id, user_id,
                                                number_of_resource, max_length)

    def delete_resource(self, resource_id):
        self.set_foreign_keys_support()
        return self.resource_repo.delete_resource(resource_id)

    def modify_resource(self, resource_id, rating):
        self.set_foreign_keys_support()
        return self.resource_repo.modify_resource(resource_id, rating)

    def create_resource(self, goal_id, user_id, title, link,
                        topic, description=None, required_time=None):
        return self.resource_repo.create_resource(goal_id, user_id, title, link,
                                                  topic, description, required_time)
