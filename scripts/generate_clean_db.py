'''
Created on 24.02.2018

This scripts uses the Engine class to remove the current database
and create a new one based on the data_dump file

WARNING: executing this scripts will remove all the current entries 
		 from the database
'''

from src.db.engine import Engine

def main():
    engine = Engine()
    engine.remove_database()
    engine.create_tables()
    engine.populate_tables()

if __name__ == '__main__':
    print('Reseting the database ...')
    main()
    print('Reseting completed. Database contains a clean image')