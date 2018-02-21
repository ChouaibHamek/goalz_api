'''
Created on 20.02.2018

Provides a series of constants used in the implementation of the db interface
'''

# Default paths for .db and .sql files to create and populate the database.
DEFAULT_DB_PATH = 'db/goalz.db'
DEFAULT_SCHEMA = "db/goalz_schema_dump.sql"
DEFAULT_DATA_DUMP = "db/goalz_data_dump.sql"

# SQL statements used in the db layer
SQL_TURN_FOREIGN_KEY_ON = "PRAGMA foreign_keys = ON"
SQL_TURN_FOREIGN_KEY_OFF = "PRAGMA foreign_keys = OFF"
SQL_DELETE_USERS_DATA = "DELETE FROM users"
SQL_DELETE_USERS_PROFILE_DATA = "DELETE FROM user_profile"
SQL_DELETE_GOALS_DATA = "DELETE FROM goals"
SQL_DELETE_RESOURCES_DATA = "DELETE FROM resources"