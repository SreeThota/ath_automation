import random
import numpy
from behave import *
import os
from utils.mysql.mysql_db_utils import MySqlDatabase
from utils.generic.FileUtilities import FileUtilities


@given('Schema {schema_name} name')
def store_schema_name_in_context(context, schema_name):
    context.schema = schema_name
    print(context.schema)
    print(os.getcwd())


@given('Table {table_name} name')
def store_schema_name_in_context(context, table_name):
    context.table_name = table_name
    print(context.table_name)


@when('I query all records of table')
def query_and_get_records(context):
    rows = MySqlDatabase.execute_query(f'select * from {context.schema}.{context.table_name}')
    context.rows = rows
    print('before insertion: ', len(context.rows))


@when('I query all records of the table after insertion')
def query_and_get_records_after_insertion(context):
    rows = MySqlDatabase.execute_query(f'select * from {context.schema}.{context.table_name}')
    context.actual_rows = rows


@when('I insert {insert_count} entry into the table')
def insert_record_into_table(context, insert_count: str):
    reference_queries = FileUtilities.read_json_file_content('mysql_reference_queries.json',
                                                             rf'utils\mysql')
    for i in range(int(insert_count)):
        query = ''
        if context.schema == 'sakila' and context.table_name == 'payment':
            query = (rf'''insert into sakila.payment (customer_id, staff_id, rental_id, amount) values(
                        customer_id_value, staff_id_value, rental_id_value, 
                        {numpy.random.randint(10, 99)}.{numpy.random.randint(10, 99)})''')
        # print(reference_queries[rf'{context.schema}.{context.table_name}'], '\n')
        for key in reference_queries[rf'{context.schema}.{context.table_name}']['ref_source']:
            rows = MySqlDatabase.execute_query(
                reference_queries[rf'{context.schema}.{context.table_name}']['ref_source'][key])
            value = rows[random.randrange(len(rows))][0]
            query = query.replace(rf'{key}_value', rf'{value}')
        row_id = MySqlDatabase.insert_record(query)
        row_after_insert = MySqlDatabase.execute_query(rf'''select * from {context.schema}.{context.table_name}
                                                       where {context.table_name}_id = {row_id}''')
        context.rows.append(row_after_insert[0])
    print('after insertion: ', len(context.rows))


@then('I verify record count matched')
def verify_records_count_matched(context):
    print('expected: ', len(context.rows))
    print('actual: ', len(context.actual_rows))
    assert len(context.rows) == len(context.actual_rows)


@when('I query duplicate records in table')
def query_duplicate_records(context):
    reference_queries = FileUtilities.read_json_file_content('mysql_reference_queries.json',
                                                             rf'utils\mysql')
    query = reference_queries[rf'{context.schema}.{context.table_name}']['pk_check']
    context.duplicate_rows = MySqlDatabase.execute_query(query)
    print(len(context.duplicate_rows))


@then('I verify no duplicates found in table')
def verify_no_duplicates(context):
    print('duplicate count: ', len(context.duplicate_rows))
    assert len(context.duplicate_rows) == 0


@then('I verify content of the table matched')
def verify_content_matched(context):
    diff = [x for x in set(context.rows).symmetric_difference(set(context.actual_rows))]
    print('diff: ', len(diff))
    assert len(diff) == 0
    # print(context.rows[0])
    # print(context.actual_rows[0])
    # print(context.rows[0] == context.actual_rows[0])
    # print(context.rows[len(context.rows) - 1])
    # print(context.actual_rows[len(context.actual_rows) - 1])
    # print(context.rows[len(context.rows) - 1] == context.actual_rows[len(context.actual_rows) - 1])
    # for i in range(len(context.rows)):
    #     assert context.rows[i] == context.actual_rows[i]


@then('I verify none of the mandatory columns holding either empty or null')
def verify_none_of_mandatory_columns_have_empty_or_null(context):
    reference_queries = FileUtilities.read_json_file_content('mysql_reference_queries.json',
                                                             rf'utils\mysql')
    mandatory_columns_queries = reference_queries[rf'{context.schema}.{context.table_name}']['mandatory_columns_check']
    for key in mandatory_columns_queries:
        print(mandatory_columns_queries[key])
        rows = MySqlDatabase.execute_query(mandatory_columns_queries[key])
        # print(rf'${context.table_name} diff', rows[0][0])
        assert rows[0][0] == 0


@then('I verify no foreign key reference issue exists')
def verify_no_fk_reference_issue_exists(context):
    reference_queries = FileUtilities.read_json_file_content('mysql_reference_queries.json',
                                                             rf'utils\mysql')
    fk_check_queries = reference_queries[rf'{context.schema}.{context.table_name}']['fk_check']
    for key in fk_check_queries:
        print(fk_check_queries[key])
        rows = MySqlDatabase.execute_query(fk_check_queries[key])
        assert rows[0][0] == 0