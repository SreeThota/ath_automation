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
            # print(connection)
        except Exception as e:
            print('Exception: ', e)
        return connection

    @staticmethod
    def execute_query(query: str):
        connection = MySqlDatabase.get_connection('root', 'Test@1234', 'localhost')
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            if 'update' in query.casefold() or 'delete' in query.casefold():
                connection.commit()
            if cursor:
                cursor.close()
            connection.close()
            return rows

    @staticmethod
    def insert_record(query: str, values=[]):
        connection = MySqlDatabase.get_connection('root', 'Test@1234', 'localhost')
        print(connection)
        insert_id = 0
        if connection:
            cursor = connection.cursor()
            if '%s' in query and len(values) == 0:
                raise Exception("Missing params to insert")
            elif '%s' in query and len(values) > 0:
                cursor.execute(query, params=values)
            elif '%s' not in query:
                cursor.execute(query)
            connection.commit()
            insert_id = cursor.lastrowid
            if cursor:
                cursor.close()
            connection.close()
        return insert_id

