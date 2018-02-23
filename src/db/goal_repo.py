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
