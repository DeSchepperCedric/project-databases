import unittest

from app.database_connection.models import DBConnection
from app.user_service.models import UserDataAccess, User
from config import *


class TestUserService(unittest.TestCase):

    def test_cmp_users(self):
        username = "test_username"
        password = "test_pass"
        firstname = "test_fname"
        lastname = "test_lname"
        email = "test_email@test.com"
        status = "user"
        active = True

        # Create user_obj to compare with self
        user_obj1 = User(username=username, password=password, firstname=firstname, lastname=lastname, email=email,
                         status=status, active=active)

        user_obj2 = User(username=username, password=password, firstname=firstname, lastname=lastname, email=email,
                         status=status, active=active)

        self.assertTrue(user_obj1 == user_obj2)

    def connect(self):
        connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_add_user(self):
        connection = self.connect()
        cursor = connection.get_cursor()

        username = "test_username"
        password = "test_pass"
        firstname = "test_fname"
        lastname = "test_lname"
        email = "test_email@test.com"
        status = "user"
        active = True

        # Create obj to access user data in db
        user_data_access_obj = UserDataAccess(dbconnect=connection)

        # Remove test_user before trying to add
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

        # Create user_obj to add to db
        user_obj = User(username=username, password=password, firstname=firstname, lastname=lastname, email=email,
                        status=status, active=active)

        # Add user to db using UserDataAccess class
        user_data_access_obj.add_user(user_obj)

        # Retrieve test_user data from db
        query = cursor.mogrify(
            'SELECT * FROM Member WHERE Username=%s;',
            (username,))
        cursor.execute(query)

        row = cursor.fetchone()

        self.assertIsNotNone(row)

        db_user_obj = User(row['username'], row['pass'], row['firstname'], row['lastname'], row['email'],
                           row['status'], row['active'])

        self.assertTrue(user_obj == db_user_obj)

        # Remove test_user after test
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

    def test_get_user(self):
        connection = self.connect()
        cursor = connection.get_cursor()

        username = "test_username"
        password = "test_pass"
        firstname = "test_fname"
        lastname = "test_lname"
        email = "test_email@test.com"
        status = "user"
        active = True

        # Create obj to access user data in db
        user_data_access_obj = UserDataAccess(dbconnect=connection)

        # Remove test_user before trying to add
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

        # Insert user into db
        query = cursor.mogrify(
            'INSERT INTO Member(Username,Pass,FirstName,LastName,Email,Status,Active) '
            'VALUES(%s,%s,%s,%s,%s,%s,%s)', (username, password, firstname, lastname, email, status, active,))
        cursor.execute(query)
        connection.commit()

        # Create user_obj to compare with db_user_obj
        user_obj = User(username=username, password=password, firstname=firstname, lastname=lastname, email=email,
                        status=status, active=active)

        # Retrieve db_user_obj using UserDataAccess class
        db_user_obj = user_data_access_obj.get_user(username)

        self.assertEqual(user_obj, db_user_obj)

        # Remove test_user after test
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

    def test_get_users(self):
        connection = self.connect()
        cursor = connection.get_cursor()

        username = "test_username"
        password = "test_pass"
        firstname = "test_fname"
        lastname = "test_lname"
        email = "test_email@test.com"
        status = "user"
        active = True

        # Create obj to access user data in db
        user_data_access_obj = UserDataAccess(dbconnect=connection)

        # Remove test_user before trying to add
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

        # Insert user into db
        query = cursor.mogrify(
            'INSERT INTO Member(Username,Pass,FirstName,LastName,Email,Status,Active) '
            'VALUES(%s,%s,%s,%s,%s,%s,%s)', (username, password, firstname, lastname, email, status, active,))
        cursor.execute(query)
        connection.commit()

        # Create user_obj to compare with db_user_obj
        user_obj = User(username=username, password=password, firstname=firstname, lastname=lastname, email=email,
                        status=status, active=active)

        # Retrieve db_user_obj using UserDataAccess class
        db_user_objs = user_data_access_obj.get_users()
        db_user_found = False

        for db_user_obj in db_user_objs:
            if db_user_obj.username == user_obj.username:
                db_user_found = True

                self.assertEqual(user_obj, db_user_obj)
                break

        self.assertTrue(db_user_found)

        # Remove test_user after test
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

    def test_login_user(self):
        connection = self.connect()
        cursor = connection.get_cursor()

        username = "test_username"
        password = "test_pass"
        firstname = "test_fname"
        lastname = "test_lname"
        email = "test_email@test.com"
        status = "user"
        active = True

        # Create obj to access user data in db
        user_data_access_obj = UserDataAccess(dbconnect=connection)

        # Remove test_user before trying to add
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

        # Insert user into db
        query = cursor.mogrify(
            'INSERT INTO Member(Username,Pass,FirstName,LastName,Email,Status,Active) '
            'VALUES(%s,%s,%s,%s,%s,%s,%s)', (username, password, firstname, lastname, email, status, active,))
        cursor.execute(query)
        connection.commit()

        # Login in user, returns password
        db_user_pass = user_data_access_obj.login_user(username)

        self.assertEqual(db_user_pass, password)

        # Remove test_user after test
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

        # Try login in using non-existant username, raises exception
        self.assertRaises(Exception, user_data_access_obj.login_user, username)

    def test_alter_user(self):
        connection = self.connect()
        cursor = connection.get_cursor()

        username = "test_username"
        password = "test_pass"
        firstname = "test_fname"
        lastname = "test_lname"
        email = "test_email@test.com"
        status = "user"
        active = True

        altered_password = "altered_test_pass"
        altered_firstname = "altered_test_fname"
        altered_lastname = "altered_test_lname"
        altered_email = "altered_est_email@test.com"
        altered_status = "admin"
        altered_active = False

        # Create obj to access user data in db
        user_data_access_obj = UserDataAccess(dbconnect=connection)

        # Remove test_user before trying to add
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()

        # Insert user into db
        query = cursor.mogrify(
            'INSERT INTO Member(Username,Pass,FirstName,LastName,Email,Status,Active) '
            'VALUES(%s,%s,%s,%s,%s,%s,%s)', (username, password, firstname, lastname, email, status, active,))
        cursor.execute(query)
        connection.commit()

        # Create altered_user_obj
        altered_user_obj = User(username=username, password=altered_password, firstname=altered_firstname,
                                lastname=altered_lastname, email=altered_email,
                                status=altered_status, active=altered_active)

        user_data_access_obj.alter_user(altered_user_obj)

        # Retrieve db_user_obj from db
        cursor.execute(
            'SELECT Username,Pass, FirstName, LastName, Email, Status, Active FROM Member WHERE Username=%s;',
            (username,))
        row = cursor.fetchone()

        self.assertIsNotNone(row)
        db_altered_user_obj = User(row['username'], row['pass'], row['firstname'], row['lastname'], row['email'],
                                   row['status'], row['active'])

        self.assertTrue(altered_user_obj == db_altered_user_obj)

        # Remove test_user after test
        cursor.execute('DELETE FROM Member WHERE UserName=%s', (username,))
        connection.commit()


if __name__ == '__main__':
    unittest.main()
