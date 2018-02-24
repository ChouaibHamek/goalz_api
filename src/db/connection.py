'''
Created on 20.02.2018

Provides the database API to access the goal tracker's persistent data.

Reference: Code taken an modified from PWP2018 exercise
'''

import sqlite3

from src.db import constants
from src.db.resource_repo import ResourceRepo
from src.db.goal_repo import GoalRepo
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
        self.goal_repo = GoalRepo(self.con)
        self.resource_repo = ResourceRepo(self.con)
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

    # USER METHODS
    def get_user(self, user_id=None, nickname=None):
        '''
        Extracts all the information of a user by user_id or nickname.

        :param integer user_id: The unique id of the user to search for, default None.
        :param string nickname: The nickname of the user to search for, default None.
        :return: dictionary with the format provided in the method:
            :py:meth:`_create_user_object`. None is returned if the database
            has no users with given user_id.
        '''
        self.set_foreign_keys_support()
        return self.user_repo.get_user(user_id, nickname)

    def get_user_public(self, user_id=None, nickname=None):
        '''
        Extracts public information of a user by the user_id or nickname
        
        :param integer user_id: The unique ID of the user, default None.
        :param string nickname: The nickname of the user to search for, default None.
        :return: user data dictionary with the format provided in the method:
            :py:meth:`_create_user_list_object`. None is returned if the database
            has no users with given nickname.
        '''
        self.set_foreign_keys_support()
        return self.user_repo.get_user_public(user_id, nickname)

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

    # GOAL METHODS
    # delegate methods from the goal_repo class
    def get_goal(self, goal_id):
        '''
        Extracts a goal from the database.

        :param goal_id: The id of the goal (int)``.
        :return: A dictionary with the format provided in
            :py:meth:`_create_goal_object` or None if the goal with target
            id does not exist.

        '''
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
