import oracledb


class OracleDatabase:
    username = ''
    password = ''
    url = ''

    @staticmethod
    def get_connection(username: str, password: str, jdbc: str):
        try:
            connection = oracledb.connect(user=username, password=password, dns=jdbc)
        except Exception as e:
            print('Exception: ', e)
        return connection

    @staticmethod
    def execute_query(query: str):
        connection = OracleDatabase.get_connection('', '', '')
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
        connection = OracleDatabase.get_connection('', '', '')
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            if cursor:
                cursor.close()
            connection.close()

# import oracledb
#
# un = 'sreenu15alfa@gmail.com'
# cs = 'livesql.oracle.com'
# pw = 'Sreenu2315#'
#
# with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
#     with connection.cursor() as cursor:
#         sql = """select sysdate from dual"""
#         for r in cursor.execute(sql):
#             print(r)
