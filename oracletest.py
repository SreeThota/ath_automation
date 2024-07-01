from utils.oracle.oracle_db_utils import OracleDatabase
from utils.mysql.mysql_db_utils import MySqlDatabase

rows = MySqlDatabase.query_and_retrieve_data('with base as (select actor_id, count(*) from sakila.actor '
                                             'group by actor_id having count(*) > 1) select count(*) from base;')
print(rows[0][0])
assert rows[0][0] == 0