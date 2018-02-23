
class ResourceRepo(object):

    def __init__(self, con):
        super(ResourceRepo, self).__init__()
        self.con = con

    def get_resource(self, resource_id):
        raise NotImplementedError("")

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
        # Transforms db row to python dictionary
        raise NotImplementedError("")

    def _create_resource_list_object(self, row):
        # Transforms db row to python dictionary
        raise NotImplementedError("")
