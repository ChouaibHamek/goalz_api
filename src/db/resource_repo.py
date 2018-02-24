import sqlite3
from src.db import constants


class ResourceRepo(object):

    def __init__(self, con):
        super(ResourceRepo, self).__init__()
        self.con = con

    def get_resource(self, resource_id):
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
        query = constants.SQL_DELETE_RESOURCE
        param_value = (resource_id,)

        cur = self.con.cursor()
        cur.execute(query, param_value)
        self.con.commit()

        if cur.rowcount < 1:
            return False
        return True

    def modify_resource(self, resource_id, rating):
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
        resource_id = row['resource_id']
        title = row['title']
        description = row['description']

        resource = {'resource_id': resource_id,
                    'title': title,
                    'description': description}

        return resource
