'''
Created on 20.02.2018

Provides the database management mechanism

Reference: Code taken an modified from PWP2018 exercise
'''

import os
import sqlite3
import src.db.constants as constants
from src.db.connection import Connection


class Engine(object):
    '''
    Abstraction of the database.

    It includes tools to create, configure, populate and connect to the sqlite file.
    It provides access to a Connection instance, and hence, to the database interface
    itself using the method :py:meth:`connection`.

    :Example:

    >>> engine = Engine()
    >>> con = engine.connect()

    :param db_path: The path of the database file (always with respect to the calling
        script. If not specified, the Engine will use the file located at *db/src.db*
    :type db_path: str
    '''

    def __init__(self, db_path=None):
        '''
        '''

        super(Engine, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = constants.DEFAULT_DB_PATH

    def connect(self):
        '''
        Creates a connection to the database.

        :return: A Connection instance
        :rtype: Connection
        '''

        return Connection(self.db_path)

    def create_tables(self, schema=None):
        '''
        Create programmatically the tables from a schema file.

        :param schema: path to the .sql schema file. If this parameter is None, then
            *db/forum_schema_dump.sql* is used.
        '''

        con = sqlite3.connect(self.db_path)
        if schema is None:
            schema = constants.DEFAULT_SCHEMA
        try:
            with open(schema, encoding="utf-8") as file:
                sql = file.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    def populate_tables(self, dump=None):
        '''
        Populate programmatically the tables from a dump file.

        :param dump:  path to the .sql dump file. If this parameter is None, then
            *db/forum_data_dump.sql* is used.
        '''

        con = sqlite3.connect(self.db_path)

        # Activate foreign keys support
        keys_on = constants.SQL_TURN_FOREIGN_KEY_ON
        cur = con.cursor()
        cur.execute(keys_on)

        # Populate database from dump
        if dump is None:
            dump = constants.DEFAULT_DATA_DUMP
        try:
            with open(dump, encoding="utf-8") as file:
                sql = file.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    def remove_database(self):
        '''
        Removes the database file from the filesystem.
        '''

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def clear(self):
        '''
        Remove all records from the database tables. Keeps the database
        schema (meaning the table structure)
        '''

        con = sqlite3.connect(self.db_path)

        #Activate foreing keys support
        keys_on = constants.SQL_TURN_FOREIGN_KEY_ON
        cur = con.cursor()
        cur.execute(keys_on)

        # Remove data from database
        with con:
            cur = con.cursor()
            cur.execute(constants.SQL_DELETE_RESOURCES_DATA)
            cur.execute(constants.SQL_DELETE_GOALS_DATA)
            cur.execute(constants.SQL_DELETE_USERS_PROFILE_DATA)
            cur.execute(constants.SQL_DELETE_USERS_DATA)

    #METHODS TO CREATE THE TABLES PROGRAMMATICALLY WITHOUT USING SQL SCRIPT
    def create_users_table(self):
        '''
        Create the table ``users`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False`` otherwise.
        '''

        return self.execute_statement(constants.SQL_CREATE_USERS_TABLE)

    def create_user_profile_table(self):
        '''
        Create the table ``user_profile`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False`` otherwise.
        '''

        return self.execute_statement(constants.SQL_CREATE_USER_PROFILE_TABLE)

    def create_goals_table(self):
        '''
        Create the table ``goals`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``otherwise.
        '''

        return self.execute_statement(constants.SQL_CREATE_GOALS_TABLE)

    def create_resources_table(self):
        '''
        Create the table ``resources`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``otherwise.
        '''

        return self.execute_statement(constants.SQL_CREATE_RESOURCE_TABLE)

    # HELPER METHODS
    def execute_statement(self, statement):
        '''
        Execute an SQL statement with foreign key support on

        :return: ``True`` if the statement was successful ``False`` otherwise.
        '''

        keys_on = constants.SQL_TURN_FOREIGN_KEY_ON
        con = sqlite3.connect(self.db_path)
        with con:
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                cur.execute(statement)
            except sqlite3.Error as excp:
                print("Error %s:" % excp.args[0])
                return False
        return True
