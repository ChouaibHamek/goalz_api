'''
Created on 23.02.2018

Provides method to access and manipulate data from the "goal" table

Reference: Code adapted and modified from PWP2018 exercise
'''
import src.db.constants as constants
import sqlite3

class GoalRepo(object):
    '''
    Methods to manipulate "goal" table in the Goalz database

    The sqlite3 connection instance is received as a constructor parameter and
    is accessible to all the methods of this class through the
    :py:attr:`self.con` attribute.

    Methods of this class **MUST** not be accessed directly. All the calls to
    the database should be made through the API provided by :py:class:`Connection`

    :param con: Connection to an SqlLite database
    :type con: sqlite3.Connection
    '''
    def __init__(self, con):
        super(GoalRepo, self).__init__()
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
        goals = {}
        for key in row.keys():
            goals[key] = row[key]
        return goals

    def _create_goal_list_object(self, row):
        '''
        Same as :py:meth:`_create_resource_object`. However, the resulting
        dictionary is targeted to build resources in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: A dictionary containing the following keys:

            * ``goal_id``: id of the goal (int)
            * ``title``: goal's title (string)
            * ``topic``: goal's topic (string)
            * ``description``: resource's description (string)
        '''
        return {
            'goal_id': row['goal_id'],
            'title': row['title'],
            'topic': row['topic'],
            'description': row['description']
        }

    def get_goal(self, goal_id):
        '''
        Extracts a goal from the database.

        :param goal_id: The id of the goal (int)``.
        :return: A dictionary with the format provided in
            :py:meth:`_create_goal_object` or None if the goal with target
            id does not exist.

        '''
        #Create the SQL Query
        query = constants.SQL_SELECT_GOAL_BY_ID
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (goal_id,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        return self._create_goal_object(row)

    def get_goals(self, user_id, number_of_goals, before, after):
        '''
        Return a list of all the goals in the database filtered by the
        conditions provided in the parameters.

        :param user_id: Search goals of a user with the given user_id.
            If this parameter is None, it returns the goals of any user in
            the system.
        :type user_id: int
        :param number_of_goals: Sets the maximum number of
            goals returning in the list. If set to None, there is no limit.
        :type number_of_goals: int
        :param before: All deadlines > ``before`` (UNIX timestamp) are removed.
            If set to None, this condition is not applied.
        :type before: long
        :param after: All deadlines < ``after`` (UNIX timestamp) are removed.
            If set to None, this condition is not applied.
        :type after: long

        :return: A list of goals. Each goal is a dictionary containing
            the following keys:

            * ``goal_id``: integer representing the Id of the goal..
            * ``title``: string containing the title of the goal.
            * ``description``: string containing the description of goal.

            Note that all values in the returned dictionary are string unless
            otherwise stated.

        :raises ValueError: if ``before`` or ``after`` are not valid UNIX
            timestamps

        '''
        #Create the SQL Statement build the string depending on the existence
        #of user_id, numbero_of_goals, before and after arguments.
        if before is not None and ( not isinstance(before, int) or before < 0):
            raise ValueError("Invalid `before` timestamps")
        if after is not None and ( not isinstance(after, int) or after < 0):
            raise ValueError("Invalid `bfter` timestamps")
        query = 'SELECT * FROM goals'
          #user_id restriction
        if (user_id is not None) or \
            (before is not None) or \
            (after  is not None):
            query += ' WHERE'
        if user_id is not None:
            query += " user_id = %s" % str(user_id)
          #Before restriction
        if before is not None:
            if user_id is not None:
                query += ' AND'
            query += " deadline < %s" % str(before)
          #After restriction
        if after is not None:
            if user_id is not None or before is not None:
                query += ' AND'
            query += " deadline > %s" % str(after)
          #Order of results
        query += ' ORDER BY deadline DESC'
          #Limit the number of resulst return
        if number_of_goals is not None:
            query += ' LIMIT ' + str(number_of_goals)
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        goals = []
        for row in rows:
            goal = self._create_goal_list_object(row)
            goals.append(goal)
        return goals

    def delete_goal(self, goal_id):
        '''
        Delete the goal with id given as parameter.

        :param int goal_id: id of the goal to remove.
        :return: True if the goal has been deleted, False otherwise

        '''
        #Create the SQL Statements
          #SQL Statement for deleting the goal entry
        query = constants.SQL_DELETE_GOAL_BY_ID
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to delete
        pvalue = (goal_id,)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that it has been deleted
        if cur.rowcount < 1:
            return False
        return True

    def modify_goal(self, goal_id, title, topic, description, deadline,
                    status):
        '''
        Modify the title, the topic, the description, the status, and the
        deadline of the goal with id ``goal_id``. An individual field can be
        modified by setting the rest as None.

        :param int goal_id: The id of the goal to remove.
        :param str title: the goal's title
        :param str topic: the goal's topic
        :param str description: the goal's description
        :param int deadline: the goal's deadline
        :param int status: the goal's status
        :return: the id of the edited goal or None if the goal was
              not found.

        '''
        #Create the SQL Statements
          #SQL Statement for modifying a goal entry
        # for readability
        _title = title is not None
        _topic = topic is not None
        _description = description is not None
        _deadline = deadline is not None
        _status = status is not None

        if _title or _topic or _description or _deadline or _status:
            query = "UPDATE goals SET "
        else:
            return None

        if _title:
            query+= "title = '%s'" % title
        if _topic:
            if _title:
                query+=", "
            query+= "topic = '%s'" % topic
        if _description:
            if _topic or _title:
                query+=", "
            query+= "description = '%s'" % description
        if _deadline:
            if _topic or _title or _description:
                query+=", "
            query+= "deadline = %s" % str(deadline)
        if _status:
            if _topic or _title or _description or _deadline:
                query+=", "
            query+= "status = %s" % str(status)

        query+= " WHERE goal_id = %s" % str(goal_id)

        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to modify
        cur.execute(query)
        self.con.commit()
        #Check that it has been modified
        if cur.rowcount < 1:
            return None
        return goal_id

    def create_goal(self, user_id, parent_id, title, topic, description,
                    deadline, status):
        '''
        Create a new goal with the data provided as arguments.

        :param int user_id: the id of the user that created the goal
        :param int parent_id: the goal's parent_id
        :param str title: the goal's title
        :param str topic: the goal's topic
        :param str description: the goal's description
        :param int deadline: the goal's deadline
        :param int status: the goal's status

        :return: the id of the created goal or None if user or parent goals
            were not found.

        '''
        if parent_id is not None:
            # Check if referred parent goal exists
            query = constants.SQL_SELECT_GOAL_BY_ID
            param_value = (parent_id,)
            cur = self.con.cursor()
            cur.execute(query, param_value)
            row = cur.fetchone()
            if row is None:
                return None

        # Check if referred user exists
        query = constants.SQL_SELECT_USER_BY_ID
        param_value = (user_id,)
        cur = self.con.cursor()
        cur.execute(query, param_value)
        row = cur.fetchone()
        if row is None:
            return None

        #Create the SQL statment
          #SQL Statement for inserting the data
        stmnt = constants.SQL_INSERT_GOAL
          #Variables for the statement.
          #user_id is obtained from first statement.
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Generate the values for SQL statement
        pvalue =  (parent_id, title, topic, description, deadline, status,
                    user_id)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added goal
        lid = cur.lastrowid
        #Return the id in
        return lid if lid is not None else None
