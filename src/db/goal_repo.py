'''
Created on 23.02.2018

Provides the database API to access the goal tracker's persistent data.

Reference: Code taken an modified from PWP2018 exercise
'''
import constants as constants

class GoalRepo(object):

    def __init__(self, con):
        super(GoalsRepo, self).__init__()
        self.con = con


    # HELPER METHODS FOR GOALS
    def _create_goal_object(self, row):
        '''
        It takes a :py:class:`sqlite3.Row` and transform it into a dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary containing the following keys:

            * ``goal_id``: id of the goal (int)
            * ``parent_id``: id of the parent goal (int)
            * ``user_id``: id of the user associated with the goal (int)
            * ``title``: goal's title (string)
            * ``topic``: goal's topic (string)
            * ``description``: goal's description (string)
            * ``deadline``: goal's set deadline (int)
            * ``status``: goal's completion status (int)

        '''
        print("inside _create_goal_object")
        goals = {}
        for key in row.keys():
            goals[key] = row[key]
        return goals

    def _create_goal_list_object(self, row):
        return {
            'goal_id': row['goal_id'],
            'title': row['title'],
            'description': row[description]
        }

    def get_goal(self, goal_id):
        raise NotImplementedError("")

    def get_goals(self, user_id, number_of_goals,
                     before, after):
         raise NotImplementedError("")

    def delete_goal(self, goal_id):
        raise NotImplementedError("")

    def modify_goal(self, goal_id, title, topic, description, deadline,
                    status):
        raise NotImplementedError("")


    def create_goal(self, title, parent_id, topic, description, deadline,
                    status):
        raise NotImplementedError("")
