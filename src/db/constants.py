'''
Created on 20.02.2018

Provides a series of constants used in the implementation of the db interface
'''

# Default paths for .db and .sql files to create and populate the database.
DEFAULT_DB_PATH = 'db/goalz.db'
DEFAULT_SCHEMA = "db/goalz_schema_dump.sql"
DEFAULT_DATA_DUMP = "db/goalz_data_dump.sql"

# SQL statements used in the db laye`r
SQL_TURN_FOREIGN_KEY_ON = "PRAGMA foreign_keys = ON"
SQL_TURN_FOREIGN_KEY_OFF = "PRAGMA foreign_keys = OFF"

# USERS statements
SQL_SELECT_USER_BY_ID = 'SELECT user_id from users WHERE user_id = ?'
SQL_SELECT_USER_BY_NICKNAME = 'SELECT user_id from users WHERE nickname = ?'
SQL_SELET_USER_AND_PROFILE_BY_ID = 'SELECT users.*, user_profile.* FROM users, user_profile \
                                    WHERE users.user_id = ? \
                                    AND user_profile.user_id = users.user_id'
SQL_SELECT_USER_AND_PROFILE = 'SELECT users.*, user_profile.* FROM users, user_profile \
                               WHERE users.user_id = user_profile.user_id'
SQL_DELETE_USER = 'DELETE FROM users WHERE user_id = ?'
SQL_DELETE_USERS_DATA = "DELETE FROM users"
SQL_DELETE_USERS_PROFILE_DATA = "DELETE FROM user_profile"
SQL_UPDATE_USER_PASSWORD = 'UPDATE users SET password = ?\
                            WHERE user_id = ?'
SQL_UPDATE_USER_PROFILE = 'UPDATE user_profile SET firstname = ?,lastname = ?, \
                            email = ?,age = ?, \
                            gender = ?,website = ? \
                            WHERE user_id = ?'
SQL_INSERT_USER = 'INSERT INTO users(nickname,password,registration_date)\
                   VALUES(?,?,?)'
SQL_INSERT_USER_PROFILE = 'INSERT INTO user_profile (user_id,firstname,lastname, \
                           email,age,gender,rating,website) \
                           VALUES (?,?,?,?,?,?,?,?)'
SQL_DELETE_USERS_DATA = "DELETE FROM users"
SQL_DELETE_USERS_PROFILE_DATA = "DELETE FROM user_profile"

# GOALS statements
SQL_DELETE_GOALS_DATA = "DELETE FROM goals"
SQL_SELECT_GOAL_BY_ID = "SELECT * FROM goals WHERE goal_id = ?"
SQL_DELETE_GOAL_BY_ID = "DELETE FROM goals WHERE goal_id = ?"
SQL_UPDATE_GOAL = "UPDATE goals SET title = ?, topic = ?, description = ?, \
                deadline = ?, status = ? WHERE goal_id = ?"
SQL_INSERT_GOAL = 'INSERT INTO goals (parent_id, title, topic, description, \
                deadline, status, user_id) VALUES(?,?,?,?,?,?,?)'
# SQL STATEMENTS FOR GET GOALS FILTERS AND UPDATE GOAL ARE IMPLEMENTED
# INSIDE GOAL_REPO FOR READABILITY AND EASE OF USE

# RESOURCES statements
SQL_DELETE_RESOURCES_DATA = "DELETE FROM resources"
SQL_SELECT_RESOURCE_BY_ID = 'SELECT * FROM resources WHERE resource_id = ?'
SQL_SELECT_RESOURCES = 'SELECT * FROM resources'
SQL_SELECT_RESOURCE_GOAL_ID_FILTER = 'goal_id = ?'
SQL_SELECT_RESOURCE_USER_ID_FILTER = 'user_id = ?'
SQL_SELECT_RESOURCE_LENGTH_FILTER = 'required_time < ?'
SQL_DELETE_RESOURCE = 'DELETE FROM resources WHERE resource_id = ?'
SQL_UPDATE_RESOURCE = 'UPDATE resources SET rating = ? WHERE resource_id = ?'
SQL_INSERT_RESOURCE = 'INSERT INTO resources (goal_id, user_id, title,' \
                      'link, topic, description, required_time, rating) \
                       VALUES(?,?,?,?,?,?,?,?)'

SQL_SELECT_USER_BY_ID = 'SELECT * from users WHERE user_id = ?'

SQL_LIMIT_CLAUSE = ' LIMIT ?'
SQL_WHERE_CLAUSE = ' WHERE '
SLQ_AND_CLAUSE = ' AND '

SQL_CREATE_USERS_TABLE = \
    'CREATE TABLE  users( \
      user_id INTEGER PRIMARY KEY,\
      nickname TEXT UNIQUE,\
      registration_date INTEGER,\
      password TEXT)'
SQL_CREATE_USER_PROFILE_TABLE = \
    'CREATE TABLE user_profile( \
      user_profile_id INTEGER PRIMARY KEY,\
      user_id INTEGER,\
      firstname TEXT,\
      lastname TEXT,\
      email TEXT,\
      website TEXT,\
      rating REAL,\
      age INTEGER,\
      gender TEXT,\
      FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE)'
SQL_CREATE_GOALS_TABLE = \
    'CREATE TABLE goals( \
      goal_id INTEGER,\
      parent_id INTEGER,\
      user_id INTEGER,\
      title TEXT,\
      topic TEXT,\
      description TEXT,\
      deadline INTEGER,\
      status INTEGER,\
      FOREIGN KEY(parent_id) REFERENCES goals(goal_id) ON DELETE CASCADE,\
      FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE)'
SQL_CREATE_RESOURCE_TABLE = \
    'CREATE TABLE IF NOT EXISTS resources(\
      resource_id INTEGER PRIMARY KEY,\
      goal_id INTEGER,\
      user_id INTEGER,\
      title TEXT,\
      link TEXT,\
      topic TEXT,\
      description TEXT,\
      required_time INTEGER,\
      rating REAL,\
      FOREIGN KEY(goal_id) REFERENCES goals(goal_id) ON DELETE CASCADE,\
      FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE SET NULL)'
