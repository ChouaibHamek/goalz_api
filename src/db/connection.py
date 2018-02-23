'''
Created on 20.02.2018

Provides the database API to access the goal tracker's persistent data.

Reference: Code taken an modified from PWP2018 exercise
'''

import sqlite3
import src.db.constants as constants
from src.db.goal_repo import GoalRepo

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
        self.goal_repo = GoalRepo(self.con)

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

    # GOAL METHODS
    # delegate methods from the goal_repo class
    def get_goal(self, goal_id):
        self.set_foreign_keys_support()
        return self.goal_repo.get_goal(goal_id)

    def get_goals(self, user_id=None, number_of_goals=None,
                     before=None, after=None):
        '''
        Return a list of all the goals in the database filtered by the
        conditions provided in the parameters.

        :param user_id: Default None. Search goals of a user with the given
            user_id. If this parameter is None, it returns the goals of any user
            in the system.
        :type user_id: int
        :param number_of_goals: Default None. Sets the maximum number of
            goals returning in the list. If set to None, there is no limit.
        :type number_of_goals: int
        :param before: Default None. All deadlines > ``before`` (UNIX timestamp)
            are removed. If set to None, this condition is not applied.
        :type before: long
        :param after: Default None. All deadlines < ``after`` (UNIX timestamp)
            are removed. If set to None, this condition is not applied.
        :type after: long

        :return: A list of goals. Each goal is a dictionary containing
            the following keys:

            * ``goal_id``: integer representing the Id of the goal.
            * ``title``: string containing the title of the goal.
            * ``description``: string containing the description of goal.

            Note that all values in the returned dictionary are string unless
            otherwise stated.

        :raises ValueError: if ``before`` or ``after`` are not valid UNIX
            timestamps

        '''
        self.set_foreign_keys_support()
        return self.goal_repo.get_goals(user_id, number_of_goals, before, after)

    def delete_goal(self, goal_id):
        '''
        Delete the goal with id given as parameter.

        :param int goal_id: id of the goal to remove.
        :return: True if the goal has been deleted, False otherwise

        '''
        self.set_foreign_keys_support()
        return self.goal_repo.delete_goal(goal_id)

    def modify_goal(self, goal_id, title=None, topic=None, description=None,
                deadline=None, status=None):
        '''
        Modify the title, the topic, the description, the status, and the
        deadline of the goal with id ``goal_id``. An individual field can be
        modified by setting the rest as None.

        :param int goal_id: the id of the goal to remove.
        :param str title: default None. The goal's title
        :param str topic: default None. The goal's topic
        :param str description: default None. The goal's description
        :param int deadline: default None. The goal's deadline
        :param int status: default None. The goal's status
        :return: the id of the edited goal or None if the goal was
              not found.

        '''
        self.set_foreign_keys_support()
        return self.goal_repo.modify_goal(goal_id, title, topic, description,
                    deadline, status)

    def create_goal(self, user_id, title, topic, description, parent_id=None,
                    deadline=None, status=0):
        '''
        Create a new goal with the data provided as arguments.

        :param int user_id: the id of the user that created the goal
        :param int parent_id: default to None. The goal's parent_id
        :param str title: the goal's title
        :param str topic: the goal's topic
        :param str description: the goal's description.
        :param int deadline: default to None. The goal's deadline.
        :param int status: default to 0. The goal's status.

        :return: the id of the created goal or None if the goal was
            not found.

        '''
        self.set_foreign_keys_support()
        return self.goal_repo.create_goal(user_id, parent_id, title, topic,
                    description, deadline, status)

    def contains_goal(self, goal_id):
        '''
        Checks if a goal is in the database.

        :param int goal_id: Id of the goal to search.
        :return: True if the goal is in the database. False otherwise.

        '''
        return self.goal_repo.get_goal(goal_id) is not None


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
