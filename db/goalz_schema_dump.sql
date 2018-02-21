PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users(
  user_id INTEGER PRIMARY KEY,
  nickname TEXT UNIQUE,
  registration_date INTEGER,
  password TEXT);
CREATE TABLE IF NOT EXISTS user_profile(
  user_profile_id INTEGER PRIMARY KEY,
  user_id INTEGER,
  firstname TEXT,
  lastname TEXT,
  email TEXT,
  website TEXT,
  rating REAL,
  age INTEGER,
  gender TEXT,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS goals(
  goal_id INTEGER PRIMARY KEY,
  parent_id INTEGER,
  user_id INTEGER,
  title TEXT,
  topic TEXT,
  description TEXT,
  deadline INTEGER,
  status INTEGER,
  FOREIGN KEY(parent_id) REFERENCES goals(goal_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS resources(
  resource_id INTEGER PRIMARY KEY,
  goal_id INTEGER,
  user_id INTEGER,
  title TEXT,
  link TEXT,
  topic TEXT,
  description TEXT,
  required_time INTEGER,
  rating REAL,
  FOREIGN KEY(goal_id) REFERENCES goals(goal_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE SET NULL);
COMMIT;
PRAGMA foreign_keys=ON;
