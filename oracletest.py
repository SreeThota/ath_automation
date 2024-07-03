from utils.oracle.oracle_db_utils import OracleDatabase
from utils.mysql.mysql_db_utils import MySqlDatabase
import random
import numpy

# rows = MySqlDatabase.query_and_retrieve_data('SELECT count(*) from sakila.payment;')
# print(rows[0][0])
print(random.randrange(100))

print(rf'{numpy.random.randint(10, 99)}.{numpy.random.randint(10, 99)}')