Goalz API - simple goal tracker
===============================

People often struggle to know which stepts they need to take in order to 
achieve their goals. Whatever their goal is, there will always be 
experienced people who have already taken the path of success before and 
are willing to share that knowledge. A key aspect of being able to achieve 
one’s goals is to know the right track. Goalz API provides functionality to 
structure and manage people's goals.

Setup
=====

Dependencies
------------
The project contains the following dependencies:
* [python3](https://docs.python.org/3/) interpreter - required to run the system (no standalone executables are provided)
* [unittest](https://docs.python.org/3/library/unittest.html) library — Unit testing framework for python3 
* [sqlite3](https://docs.python.org/3.6/library/sqlite3.html) library — DB-API 2.0 interface for SQLite databases
* [SQlite](https://www.sqlite.org/index.html) engine - standalone sqlite distribution used for manual tests (provided with the project)
	
Configuration
-------------
If all the dependencies are in place, no additional steps must be taken to setup the project.

Database
--------
The distribution contains a clean .db file in the db folder. At any time, to return to this clean version of the database 
one can execute the script "scripts/generate_clean_db.py", from the main folder, using the command:

```
python -m scripts.generate_clean_db
```

Running the tests
=================

All tests
-------------

In order to run all the tests of the system one can execute the scripts "scripts/run_full_test_suite.py", from the main
folder, using the command:

```
python -m scripts.run_full_test_suite
```

Database tests
-------------

To test only some parts of the database api the following test files are provided:
* database_api_tests_tables.py - test methods that manage database tables and database connection
* database_api_tests_user.py - tests all methods which manipulate users' data
* database_api_tests_goal.py - tests all methods which manipulate goals' data
* database_api_tests_resources.py - tests all methods which manipulate resources' data

In order to run any of these tests one has to execute, from the main folder, the following command:

```
python -m test.<test_file>
```
	
in which the placeholder is replaced with the name of the file without the '.py' extension
