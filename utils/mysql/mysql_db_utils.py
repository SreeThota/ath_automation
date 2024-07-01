import mysql.connector

"""
Required: username, password, host (localhost for example), port
"""


class MySqlDatabase:

    @staticmethod
    def get_connection(username: str, password: str, host: str, port=3306):
        connection = None
        try:
            connection = mysql.connector.connect(user=username, password=password, host=host, port=port)
            print(connection)
        except Exception as e:
            print('Exception: ', e)
        return connection

    @staticmethod
    def query_and_retrieve_data(query: str):
        connection = MySqlDatabase.get_connection('root', 'Test@1234', 'localhost')
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            if cursor:
                cursor.close()
            connection.close()
            return rows

    @staticmethod
    def perform_dml_operation(query: str):
        connection = MySqlDatabase.get_connection('', '', '')
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            if cursor:
                cursor.close()
            connection.close()
