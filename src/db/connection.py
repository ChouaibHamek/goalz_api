'''
Created on 20.02.2018

Provides the database API to access the goal tracker's persistent data.

Reference: Code taken an modified from PWP2018 exercise
'''

import sqlite3
import src.db.constants as constants


class Connection(object):
    '''
    API to access the Goalz database.

    The sqlite3 connection instance is accessible to all the methods of this
    class through the :py:attr:`self.con` attribute.

    An instance of this class should not be instantiated directly using the
    constructor. Instead use the :py:meth:`Engine.connect`.

    Use the method :py:meth:`close` in order to close a connection.
    A :py:class:`Connection` **MUST** always be closed once when it is not going to be
    utilized anymore in order to release internal locks.

    :param db_path: Location of the database file.
    :type db_path: str
    '''

    def __init__(self, db_path):
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)
        self._isclosed = False

    def isclosed(self):
        '''
        :return: ``True`` if connection has already being closed.
        '''

        return self._isclosed

    def close(self):
        '''
        Closes the database connection, committing all changes.
        '''

        if self.con and not self._isclosed:
            self.con.commit()
            self.con.close()
            self._isclosed = True

    def check_foreign_keys_status(self):
        '''
        Check if the foreign keys has been activated.

        :return: ``True`` if  foreign_keys is activated and ``False`` otherwise.
        :raises sqlite3.Error: when a sqlite3 error happen. In this case the
            connection is closed.
        '''

        try:
            cur = self.con.cursor()
            cur.execute('PRAGMA foreign_keys')
            data = cur.fetchone()
            is_activated = data == (1,)
            print("Foreign Keys status: %s" % 'ON' if is_activated else 'OFF')
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            self.close()
            raise excp

        return is_activated

    def set_foreign_keys_support(self):
        '''
        Activate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.
        '''

        keys_on = constants.SQL_TURN_FOREIGN_KEY_ON
        try:
            cur = self.con.cursor()
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    def unset_foreign_keys_support(self):
        '''
        Deactivate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.
        '''

        keys_on = constants.SQL_TURN_FOREIGN_KEY_OFF
        try:
            cur = self.con.cursor()
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    # TODO: Add methods to manage Db data and helpers to translate that data to python dictionaries