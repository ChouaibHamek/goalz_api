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
        '''
        Extracts a resource from the database.

        In order to maintain a clear separation of responsibilities this method
        delegates the execution to the corresponding method from
        :py:class:`ResourceRepo' and returns the result

        :param int resource_id: Id of the resource to be retrieved
        :return: A dictionary with the format provided bellow or None if the resource with target
            id does not exist.

            * ``resource_id``: id of the resource (int)
            * ``goal_id``: id of the goal to which this resource was attached (int)
            * ``user_id``: id of the user who posted this resource (int)
            * ``title``: resource's title (string)
            * ``link``: location of the resource provided as web URL (string)
            * ``topic``: resource's topic (string)
            * ``description``: resource's description (string)
            * ``required_time``: number of minutes to assimilate the resource (int)
            * ``rating``: resource's rating (float)
        '''

        self.set_foreign_keys_support()
        return self.resource_repo.get_resource(resource_id)

    def get_resources(self, goal_id=None, user_id=None,
                      number_of_resource=None, max_length=None):
        '''
        Return a list of all the resources in the database filtered by the
        conditions provided in the parameters.

        In order to maintain a clear separation of responsibilities this method
        delegates the execution to the corresponding method from
        :py:class:`ResourceRepo' and returns the result

        :param goal_id: Default is None. Search resources of the goal with the given goal_id.
                        If this parameter is None, it returns the resources of
                        all the goals in the system.
        :type goal_id: int
        :param user_id: Default is None. Search resources of the user with the given user_id.
                        If this parameter is None, it returns the resources of
                        all the users in the system.
        :type user_id: int
        :param number_of_resource: Default is None. Sets the maximum number of resources to return
                                   in the list. If set to None, there is no limit.
        :type number_of_resource: int
        :param max_length: Default is None. All resources with a required time to complete greater
                           than max_length are removed. If is set to None, this
                           condition is not applied
        :type max_length: int

        :return: A list of resources. Each resource is a dictionary of items with the
                 following format

                 * ``resource_id``: id of the resource (int)
                 * ``title``: resource's title (string)
                 * ``description``: resource's description (string)
        '''

        self.set_foreign_keys_support()
        return self.resource_repo.get_resources(goal_id, user_id,
                                                number_of_resource, max_length)

    def delete_resource(self, resource_id):
        '''
        Delete the resource with id given as parameter.

        In order to maintain a clear separation of responsibilities this method
        delegates the execution to the corresponding method from
        :py:class:`ResourceRepo' and returns the result

        :param int resource_id: Id of the resource to remove.
        :return: True if the resource has been deleted, False otherwise
        '''

        self.set_foreign_keys_support()
        return self.resource_repo.delete_resource(resource_id)

    def modify_resource(self, resource_id, rating):
        '''
        Modify the rating of the resource with id ``resource_id``

        In order to maintain a clear separation of responsibilities this method
        delegates the execution to the corresponding method from
        :py:class:`ResourceRepo' and returns the result

        :param int resource_id: The id of the resource to modify.
        :param rating: The resource's rating
        :type rating: float
        :return: The id of the modified resource or None. None is returned
                 if the resource was not found or if the rating parameter is
                 not a float value.
        '''

        self.set_foreign_keys_support()
        return self.resource_repo.modify_resource(resource_id, rating)

    def create_resource(self, goal_id, user_id, title, link,
                        topic, description=None, required_time=None):
        '''
        Create a new resource with the data provided as arguments.

        In order to maintain a clear separation of responsibilities this method
        delegates the execution to the corresponding method from
        :py:class:`ResourceRepo' and returns the result

        :param int goal_id: Id of the goal for which the resource was posted
        :param int user_id: Id of the user who posted the resource
        :param str title: The title of the resource
        :param str link: The resource's web URL
        :param str topic: The topic of the resource provided as text
        :param str description: Default = None. The description of the request
        :param str description: Default = None. Estimate of the number of minutes required
                                to assimilate the resource

        :return: the id of the created message or None. None is returned if
                 the resource was not found, or the specified goal does not
                 exists in the database, or the specified user does not
                 exist in the database
        '''

        self.set_foreign_keys_support()
        return self.resource_repo.create_resource(goal_id, user_id, title, link,
                                                  topic, description, required_time)

    def contains_resource(self, resource_id):
        '''
        Checks if a resource is in the database.

        :param str resource_id: Id of the resource to search.
        :return: True if the resource is in the database. False otherwise.
        '''

        return self.get_resource(resource_id) is not None
