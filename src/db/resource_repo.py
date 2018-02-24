'''
Created on 23.02.2018

Provides method to access and manipulate data from the "resource" table

Reference: Code taken an modified from PWP2018 exercise
'''

import sqlite3
from src.db import constants


class ResourceRepo(object):
    '''
    Methods to manipulate "resource" table in the Goalz database

    The sqlite3 connection instance is received as a constructor parameter and
    is accessible to all the methods of this class through the
    :py:attr:`self.con` attribute.

    Methods of this class **MUST** not be accessed directly. All the calls to
    the database should be made through the API provided by :py:class:`Connection`

    :param con: Connection to an SqlLite database
    :type con: sqlite3.Connection
    '''

    def __init__(self, con):
        super(ResourceRepo, self).__init__()
        self.con = con

    def get_resource(self, resource_id):
        '''
        Extracts a resource from the database.

        :param int resource_id: Id of the resource to be retrieved
        :return: A dictionary with the format provided in
            :py:meth:`_create_message_object` or None if the resource with target
            id does not exist.
        '''

        query = constants.SQL_SELECT_RESOURCE_BY_ID
        param_value = (resource_id,)

        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(query, param_value)

        row = cur.fetchone()
        if row is None:
            return None
        return self._create_resource_object(row)

    def get_resources(self, goal_id, user_id, number_of_resource, max_length):
        '''
        Return a list of all the resources in the database filtered by the
        conditions provided in the parameters.

        :param goal_id: Search resources of the goal with the given goal_id. 
                        If this parameter is None, it returns the resources of
                        all the goals in the system.
        :type goal_id: int
        :param user_id: Search resources of the user with the given user_id. 
                        If this parameter is None, it returns the resources of
                        all the users in the system.
        :type user_id: int
        :param number_of_resource: Sets the maximum number of resources to return
                                   in the list. If set to None, there is no limit.
        :type number_of_resource: int
        :param max_length: All resources with a required time to complete greater
                           than max_length are removed. If is set to None, this 
                           condition is not applied
        :type max_length: int

        :return: A list of resources. Each resource is a dictionary of items as
                 created by :py:meth:`_create_message_object`
        '''

        query = constants.SQL_SELECT_RESOURCES

        filters = []
        parameters = []

        if goal_id is not None:
            if not isinstance(goal_id, int):
                return None
            filters.append(constants.SQL_SELECT_RESOURCE_GOAL_ID_FILTER)
            parameters.append(str(goal_id))
        if user_id is not None:
            if not isinstance(user_id, int):
                return None
            filters.append(constants.SQL_SELECT_RESOURCE_USER_ID_FILTER)
            parameters.append(str(user_id))
        if max_length is not None:
            if not isinstance(max_length, int):
                return None
            filters.append(constants.SQL_SELECT_RESOURCE_LENGTH_FILTER)
            parameters.append(str(max_length))
        if len(filters) != 0:
            query += constants.SQL_WHERE_CLAUSE + constants.SLQ_AND_CLAUSE.join(filters)

        if number_of_resource is not None:
            if not isinstance(number_of_resource, int):
                return None
            query += constants.SQL_LIMIT_CLAUSE
            parameters.append(str(number_of_resource))

        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(query, tuple(parameters))

        rows = cur.fetchall()
        if rows is None:
            return None

        resources = []
        for row in rows:
            resource = self._create_resource_list_object(row)
            resources.append(resource)
        return resources

    def delete_resource(self, resource_id):
        '''
        Delete the resource with id given as parameter.

        :param int resource_id: Id of the resource to remove.
        :return: True if the resource has been deleted, False otherwise
        '''

        query = constants.SQL_DELETE_RESOURCE
        param_value = (resource_id,)

        cur = self.con.cursor()
        cur.execute(query, param_value)
        self.con.commit()

        if cur.rowcount < 1:
            return False
        return True

    def modify_resource(self, resource_id, rating):
        '''
        Modify the rating of the resource with id ``resource_id``

        :param int resource_id: The id of the resource to modify.
        :param rating: The resource's rating
        :type rating: float
        :return: The id of the modified resource or None. None is returned
                 if the resource was not found or if the rating parameter is
                 not a float value.
        '''

        cur = self.con.cursor();

        # Part 1 - check if message exists
        query = constants.SQL_SELECT_RESOURCE_BY_ID
        param_value = (resource_id,)
        cur.execute(query, param_value)

        row = cur.fetchone()
        if row is not None:
            # Part 2 - execute update
            if not isinstance(rating, float):
                return None
            query = constants.SQL_UPDATE_RESOURCE
            param_value = (rating, resource_id)
            cur.execute(query, param_value)
            self.con.commit()

            if cur.rowcount > 0:
                return resource_id

        return None

    def create_resource(self, goal_id, user_id, title,
                        link, topic, description, required_time):
        '''
        Create a new resource with the data provided as arguments.

        :param int goal_id: Id of the goal for which the resource was posted
        :param int user_id: Id of the user who posted the resource
        :param str title: The title of the resource
        :param str link: The resource's web URL
        :param str topic: The topic of the resource provided as text
        :param str description: The description of the request
        :param str description: Estimate of the number of minutes required
                                to assimilate the resource

        :return: the id of the created message or None. None is returned if
                 the resource was not found, or the specified goal does not
                 exists in the database, or the specified user does not
                 exist in the database
       '''

        # Check if required_time is a number
        if required_time and not isinstance(required_time, int):
                return None

        # Check if referred goal exists
        query = constants.SQL_SELECT_GOAL_BY_ID
        param_value = (goal_id,)
        cur = self.con.cursor()
        cur.execute(query, param_value)
        row = cur.fetchone()
        if row is None:
            return None

        # Check if referred goal exists
        query = constants.SQL_SELECT_USER_BY_ID
        param_value = (user_id,)
        cur = self.con.cursor()
        cur.execute(query, param_value)
        row = cur.fetchone()
        if row is None:
            return None

        statement = constants.SQL_INSERT_RESOURCE
        param_value = (goal_id, user_id, title, link, topic,
                       description, required_time, 0)

        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(statement, param_value)
        self.con.commit()

        return cur.lastrowid

    # HELPERS FOR GOALS
    def _create_resource_object(self, row):
        '''
        It takes a :py:class:`sqlite3.Row` and transform it into a dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: A dictionary containing the following keys:

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

        resource_id = row['resource_id']
        goal_id = row['goal_id']
        user_id = row['user_id']
        title = row['title']
        link = row['link']
        topic = row['topic']
        description = row['description']
        required_time = row['required_time']
        rating = row['rating']

        resource = {'resource_id': resource_id, 'goal_id': goal_id,
                    'user_id': user_id, 'title': title,
                    'link': link, 'topic': topic, 'description': description,
                    'required_time': required_time, 'rating': rating}

        return resource

    def _create_resource_list_object(self, row):
        '''
        Same as :py:meth:`_create_resource_object`. However, the resulting
        dictionary is targeted to build resources in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: A dictionary containing the following keys:

            * ``resource_id``: id of the resource (int)
            * ``title``: resource's title (string)
            * ``description``: resource's description (string)
        '''

        resource_id = row['resource_id']
        title = row['title']
        description = row['description']

        resource = {'resource_id': resource_id,
                    'title': title,
                    'description': description}

        return resource
