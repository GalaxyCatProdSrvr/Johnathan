import mysql.connector
import sqlite3
class DatabaseConnector:
    def __init__(self):
        with sqlite3.connect('lib/JohnWick.sqlite3') as AuthDatabase:
            cursor = AuthDatabase.cursor()

        # Assuming 'Auth' table structure: Mysql_host, Mysql_username, Mysql_database, etc.
        # Select the first (or only) record from the 'Auth' table
        cursor.execute('SELECT * FROM Auth LIMIT 1')
        row = cursor.fetchone()

        # Check if a row is returned
        if row:
            # Assuming column names: Mysql_host, Mysql_username, Mysql_database, etc.
            mysql_host, mysql_username, mysql_password, mysql_port, mysql_database = row

            # Print or use the retrieved values
            # print("MySQL Host:", mysql_host)
            # print("MySQL Username:", mysql_username)
            # print("MySQL Database:", mysql_database)
        else:
            print("No records found in 'Auth' table.")

        # Close the cursor and connection
        cursor.close()
        AuthDatabase.close()


        self.user = mysql_username
        self.password = mysql_password
        self.host = mysql_host
        self.database = mysql_database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )
            print("Connected to the database!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from the database.")
        else:
            print("No active connection to disconnect.")

    def execute_query(self, query, params=None):
        if self.connection is None:
            self.connect()
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()

            return result
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
        finally:
            self.connection.commit()
            cursor.close()
            #self.disconnect()
    def get_setting(self, server_id, table_name, setting_name, default=None):
        query_result = self.execute_query(f'SELECT {setting_name} FROM {table_name} WHERE server_id = %s', (server_id,))
        if query_result and query_result[0]:
            return query_result[0][0]
        else:
            self.add_server_to_table(server_id=server_id, table_name=table_name)
            return default

    def add_server_to_table(self, server_id, table_name):
        print("adding server to database")
        # we need to check if the server ID is entered in the database first, if so then update that record, else it will create 2 records
        self.connection.cursor().execute(f'INSERT INTO {table_name} (server_id) VALUES (%s)', (server_id,))
        self.connection.commit()  # Commit changes
        print("added server to database")
