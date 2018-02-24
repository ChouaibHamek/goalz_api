'''
Created on 24.02.2018

This scripts run the entire test suite for the system

Reference: Code taken and adapted from 
           https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory
           accessed in 24.02.2018
'''

import unittest

testmodules = [
    'test.database_api_tests_resources',
    'test.database_api_tests_goal',
    'test.database_api_tests_user',
    'test.database_api_tests_tables'
    ]

def main():
    suite = unittest.TestSuite()
    for test in testmodules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    print('Start running test suite')
    main()