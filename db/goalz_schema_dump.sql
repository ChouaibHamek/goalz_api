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
  rating INTEGER,
  age INTEGER,
  gender TEXT,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS goals(
  goal_id INTEGER,
  title TEXT,
  topic TEXT,
  description TEXT,
  deadline TEXT,
  status INTEGER,
  user_id INTEGER,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS resources(
  resource_id INTEGER PRIMARY KEY,
  goal_id TEXT,
  user_id INTEGER,
  title TEXT,
  link TEXT,
  topic TEXT,
  description TEXT,
  register_date TEXT,
  rating INTEGER,
  FOREIGN KEY(goal_id) REFERENCES goals(goal_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE SET NULL);
CREATE TABLE IF NOT EXISTS goals_subgoals(
  goal_id TEXT,
  subgoal_id INTEGER,
  FOREIGN KEY(goal_id) REFERENCES goals(goal_id) ON DELETE SET NULL,
  FOREIGN KEY(subgoals_id) REFERENCES users(user_id) ON DELETE SET NULL);
COMMIT;
PRAGMA foreign_keys=ON;
