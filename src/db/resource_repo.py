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

    def get_resources_for_goal(self, goal_id, number_of_resource, max_length):
        raise NotImplementedError("")

    def get_resources_for_user(self, user_id, number_of_resource, max_length):
        raise NotImplementedError("")

    def delete_resource(self, resource_id):
        raise NotImplementedError("")

    def modify_resource(self, rating):
        raise NotImplementedError("")

    def create_resource(self, goal_id, user_id, title, link, topic, description, required_time):
        raise NotImplementedError("")

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
