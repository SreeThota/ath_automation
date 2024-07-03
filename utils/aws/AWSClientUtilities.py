import botocore
import os
import subprocess
import psycopg2
import json
from utils.generic import FileUtilities
from botocore.exceptions import NoCredentialsError


class AWSClientUtilities:
    """
    profile_name: The AWS profile name which you would like to login. Note: This name varies from person to person
    """
    @staticmethod
    def login_aws_profile(profile_name: str):
        try:
            subprocess.run(
                ["aws", "sso", "login", "--profile", profile_name],
                text=True,
                check=True,
            )
            print("AWS SSO login was successful.")
        except subprocess.CalledProcessError as e:
            print(f"Error login AWS SSO: {e}")

    """
    Copies one object to another object in same bucket
    """

    @staticmethod
    def copy_object(
        client_s3, bucket_name, object_name: str, old_file_name: str, new_file_name: str
    ):
        file_object = (
            (object_name + "/" + old_file_name) if object_name != "" else old_file_name
        )
        target_name = (
            (object_name + "/" + new_file_name) if object_name != "" else new_file_name
        )
        print(
            "Copying file "
            + file_object
            + " with name "
            + target_name
            + " in bucket: "
            + bucket_name
        )
        try:
            response = client_s3.copy_object(
                Bucket=bucket_name, CopySource=file_object, Key=target_name
            )
            print("File copied successfully")
            return response
        except Exception as e:
            print("Exception occurred while copying file: " + e)

    """
    Copies object from source bucket to target bucket
    """

    @staticmethod
    def copy_object_to_another_bucket(
        client_s3,
        origin_bucket_name: str,
        origin_object: str,
        origin_file_name: str,
        target_bucket_name: str,
        target_object: str,
        target_file_name: str,
    ):
        source = {
            "Bucket": origin_bucket_name,
            "Key": (
                (origin_object + "/" + origin_file_name)
                if origin_object != ""
                else origin_file_name
            ),
        }
        print("source: " + source)
        target_object_name = (
            (target_object + "/" + target_file_name)
            if target_object != ""
            else target_file_name
        )
        print("copying object to: " + target_object_name)
        try:
            response = client_s3.copy(source, target_bucket_name, target_object_name)
            print("Copied object successfully")
            return response
        except Exception as e:
            print("Exceptipn occurred while copying file: " + e)

    """
    client_s3: Is an connection with respective s3 client
    bucket_name: The bucket name which you are intend to access
    object: the object full path. In case we have multiple objects, all needs to be included as one value 
        (for ex: stage=landed/feed=fullLis)
    file_name_in_s3: The file name which we would like to download from s3
    destination_folder: Local folder name where you would like to save the file (/ at start and end is must)
    destination_file_name: The name with which you would like to save the file in destination folder
    """

    @staticmethod
    def download_file_object_from_s3(
        client_s3,
        bucket_name: str,
        object: str,
        file_name_in_s3: str,
        destination_folder: str,
        destination_file_name: str,
    ):
        file_name = (object + file_name_in_s3) if object != "" else file_name_in_s3
        # if object != "":
        #     file_name = object + file_name_in_s3
        # else:
        #     file_name = file_name_in_s3
        print("file_name: ", file_name)
        path = os.path.join(os.getcwd(), destination_folder, destination_file_name)
        with open(path, "wb") as f:
            client_s3.download_fileobj(bucket_name, file_name, f)

    """
    client_s3: Is an connection with respective s3 client
    bucket_name: The bucket name which you are intend to access
    file_directory: The local directory where our file exists (just directory name. For ex: dir1/childDir)
    local_file_name: The file which we would like to upload to s3
    file_key_in_s3: the object full path. In case we have multiple objects, all needs to be included as one value 
        (for ex: stage=landed/feed=fullLis)

    This method supports both upload_file and put_object operations
    """

    @staticmethod
    def upload_file_to_s3(
        client_s3,
        bucket_name: str,
        local_file_name: str,
        file_directory="",
        file_key_in_s3="",
    ):
        path = os.path.join(os.getcwd(), file_directory, local_file_name)
        print("path: ", path)
        file_key_in_s3 = file_key_in_s3 + local_file_name
        print("file key: ", file_key_in_s3)
        try:
            response = client_s3.upload_file(path, bucket_name, file_key_in_s3)
            print("File uplaoding is in progress")
            return response
        except botocore.exceptions.ClientError as e:
            print("Error received while uploading a file to bucket: " + bucket_name)
            print("Error message: " + e)

    """
    client_s3: Is an connection with respective s3 client
    bucket_name: The bucket name which you are intend to access
    file_key_to_delete: file path in s3 which we required to delete
    """

    @staticmethod
    def delete_file_from_s3(client_s3, bucket_name: str, file_key_to_delete: str):
        print("Deleting file: " + file_key_to_delete + " from bucket: " + bucket_name)
        try:
            response = client_s3.delete_object(
                Bucket=bucket_name, key=file_key_to_delete
            )
            print("File delete successful")
            return response
        except botocore.exceptions.ClientError as e:
            print("Error received while deleting a file to bucket: " + bucket_name)
            print("Error message: " + e)

    """
    Deletes multiple objects from s3 bucket
    """

    @staticmethod
    def delete_files_from_s3(client_s3, bucket_name: str, array_of_objects: list):
        if type(array_of_objects) is not list:
            print("Expected List Of Objects to delete")
            return
        try:
            response = client_s3.delete_objects(
                Bucket=bucket_name, Delete=array_of_objects
            )
            print("Deleted objects successfully")
            return response
        except Exception as e:
            print(
                "Error received while deleting multiple objects from bucket: "
                + bucket_name
            )

    """
    Retrieves object details from s3 bucket
    """

    @staticmethod
    def get_object_details(client_s3, bucket_name: str, object_name: str):
        try:
            response = client_s3.get_object(Bucket=bucket_name, Key=object_name)
            return response
        except Exception as e:
            print("Exception while reading object details: " + e)

    """
    Retrieves all available buckets associated with the client
    """

    @staticmethod
    def get_all_buckets_available_with_client(client_s3):
        try:
            response = client_s3.list_buckets()
            return response["Buckets"]
        except Exception as e:
            print("Exception occurred while getting available buckets in client: " + e)

    """
    Returns file details if exists in s3
    If file does not exists, we will get botocore.exceptions.ClientError
    """

    @staticmethod
    def is_file_exists_in_s3(client_s3, bucket_name: str, file_key: str):
        try:
            response = client_s3.head_object(Bucket=bucket_name, Key=file_key)
            print(response)
            return True
        except Exception as e:
            return False

    """
    client_athena: athena client connection like boto3.client('athena')
    workgroup: 
    db: The database with which you would like to connect
    table: The table name from which you would like to query
    column_name_to_query: On which column you would like to apply where condition
    column_value_to_query: The complete initial file which we uploaded to 'landed'. 
        For ex: file_name='s3://<bucketname>/stage=landed/feed=fan_fullhist/<Fanfile>'
    column_name_to_retrieve: Which column value we need to export
    """

    @staticmethod
    def connect_athena_get_parquet_file(
        client_athena,
        workgroup: str,
        db: str,
        table: str,
        column_name_to_query: str,
        column_value_to_query: str,
        column_name_to_retrieve: str,
    ):
        query = f"SELECT {column_name_to_retrieve} FROM {db}.{table} where {column_name_to_query}='{column_value_to_query}'"
        print(query)
        try:
            response = client_athena.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": db},
                WorkGroup=workgroup,
            )
            result = []
            while True:
                query_status = client_athena.get_query_execution(
                    QueryExecutionId=response["QueryExecutionId"]
                )
                # print("query_status: ", query_status)
                query_execution_status = query_status["QueryExecution"]["Status"][
                    "State"
                ]
                print("query_execution_status: ", query_execution_status)
                if query_execution_status == "SUCCEEDED":
                    res = client_athena.get_query_results(
                        QueryExecutionId=response["QueryExecutionId"],
                        MaxResults=2,
                        # I am limiting result rows to 2 as we just need file name from this method
                    )
                    # print(len(res["ResultSet"]["Rows"]))
                    for row in res["ResultSet"]["Rows"]:
                        if "Data" in row and len(row["Data"]) > 0:
                            result.append(row["Data"][0]["VarCharValue"])
                    break
            # print(result)
            if len(result) < 2:
                print("NO PARQUET FILE FOUND FOR THE GIVEN FEED")
            return result[1] if len(result) > 1 else None
        except botocore.exceptions.ClientError as e:
            print("Error occurred while accessing athena DB: ", e)

    """
    client_athena: athena client connection like boto3.client('athena')
    workgroup: 
    db: The database with which you would like to connect
    table: The table name from which you would like to query
    column_name_to_query: On which column you would like to apply where condition
    column_value_to_query: The complete initial file which we uploaded to 'landed'. 
        For ex: file_name='s3://<bucketname>/stage=landed/feed=fan_fullhist/<Fanfile>'
    """

    @staticmethod
    def connect_athena_get_matching_results(
        client_athena,
        workgroup: str,
        db: str,
        table: str,
        column_name_to_query: str,
        column_value_to_query: str,
    ):
        query = f"SELECT * FROM {db}.{table}  where {column_name_to_query}='{column_value_to_query}'"
        print(query)
        try:
            response = client_athena.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": db},
                WorkGroup=workgroup,
            )
            result = []
            while True:
                query_status = client_athena.get_query_execution(
                    QueryExecutionId=response["QueryExecutionId"]
                )
                # print("query_status: ", query_status)
                query_execution_status = query_status["QueryExecution"]["Status"][
                    "State"
                ]
                print("query_execution_status: ", query_execution_status)
                if query_execution_status == "SUCCEEDED":
                    is_next_results_available = True
                    while is_next_results_available:
                        res = client_athena.get_query_results(
                            QueryExecutionId=response["QueryExecutionId"]
                            # , MaxResults=3
                            # we can limit number of rows per query execution using MaxResults param
                        )
                        # print(len(res["ResultSet"]["Rows"]))
                        rows = res["ResultSet"]["Rows"]
                        columns = rows[0]
                        for index in range(1, len(rows)):
                            row = {}
                            for local_index in range(len(rows[index]["Data"])):
                                local_row = rows[index]["Data"][local_index]
                                row[columns["Data"][local_index]["VarCharValue"]] = (
                                    local_row["VarCharValue"]
                                    if "VarCharValue" in local_row
                                    else ""
                                )
                            result.append(row)
                        is_next_results_available = "NextToken" in res
                    break
            return result
        except botocore.exceptions.ClientError as e:
            print("Error occurred while accessing athena DB: ", e)

    """
    returns all th objects matching with the object name as prefix.
    """

    @staticmethod
    def list_all_matching_objects_in_s3(
        client_s3, bucket_name: str, object_name="", delimitor="/"
    ):
        try:
            data = client_s3.list_objects_v2(
                Bucket=bucket_name, Prefix=object_name, Delimiter=delimitor
            )
            if data["KeyCount"] == 0:
                print("****Found 0 records with the given prefix****")
                return []
            else:
                return data["Contents"]
        except Exception as e:
            print("Error received while listing all objects from s3 ", e)

    """
    returns the file with the last modified date 
    """

    @staticmethod
    def get_latest_file(s3_client, bucket_name, prefix):
        try:
            # List objects in the specified bucket and prefix
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

            list_object_key = [obj["Key"] for obj in response.get("Contents", [])]

            latest_format_file = max(
                list_object_key,
                key=lambda x: s3_client.head_object(Bucket=bucket_name, Key=x)[
                    "LastModified"
                ],
            )
            print(f"Last Modified: {latest_format_file}")
            return latest_format_file

        except NoCredentialsError:
            print("Credentials not available")
            return None

    @staticmethod
    def if_aws_session_expired(profile_name: str):
        """
        Check if the AWS SSO session is still active for the given AWS CLI profile.
        If the session has expired, reactivate it.

        Parameters:
        - profile_name (str): AWS CLI profile name.

        Returns:
        - None
        """
        try:
            subprocess.run(
                ["aws", "s3", "ls", "--profile", profile_name],
                text=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(f"AWS SSO is active for {profile_name}.")
        except subprocess.CalledProcessError as e:
            print(f"AWS SSO Error: {e}")

            if "status 255" in str(e):
                # The session has expired, reactivate it
                print(f"AWS SSO session reactivated for {profile_name}...")
                AWSClientUtilities.login_aws_profile(profile_name)
            else:
                print("Unhandled error during AWS SSO check.")

    @staticmethod
    def get_temp_credential(profile_name: str, workgroup_name: str) -> tuple:
        """
        Get temporary credentials using AWS SSO.

        Parameters:
        - profile_name (str): AWS CLI profile name.
        - workgroup_name (str): AWS Redshift serverless workgroup name.

        Returns:
        - tuple: A tuple containing the extracted database password and user.
        """
        # Check if AWS expired
        AWSClientUtilities.if_aws_session_expired(profile_name=profile_name)

        # AWS CLI command to get credentials
        aws_command = f"aws redshift-serverless --profile={profile_name} get-credentials --workgroup-name {workgroup_name}"

        # Execute the command and capture the output
        output = subprocess.check_output(aws_command, shell=True)

        # Load the output as JSON
        credentials = json.loads(output)

        # Extract the dbPassword and dbUser
        db_password = credentials.get("dbPassword", "")
        db_user = credentials.get("dbUser", "")

        return db_password, db_user

    @staticmethod
    def redshift_query(
        profile_name: str,
        workgroup: str,
        aws_sso_account_id: str,
        query: str,
        aws_region: str = "us-east-1",
        database: str = "nfl-dna-gridiron-dev",
    ) -> tuple:
        """
        Execute a Redshift query using temporary credentials obtained from AWS SSO.

        Parameters:
        - profile_name (str): AWS CLI profile name.
        - workgroup (str): Redshift serverless workgroup name.
        - aws_sso_account_id (str): AWS SSO account ID.
        - query (str): SQL query to be executed.
        - aws_region (str): AWS region (default: 'us-east-1').
        - database (str): Redshift database name (default: 'nfl-dna-gridiron-dev').

        Returns:
        - tuple: A tuple containing the query results (as a list of tuples) and column headers.
        """
        password, user = AWSClientUtilities.get_temp_credential(profile_name, workgroup)
        print("Get temporary credentials...")

        # Set up the Redshift connection using psycopg2
        print("Connecting to Redshift...")
        redshift_connection = psycopg2.connect(
            host=f"{workgroup}.{aws_sso_account_id}.{aws_region}.redshift-serverless.amazonaws.com",
            port=5439,
            user=user,
            password=password,
            database=database,
        )

        print("Retrieving Data...")
        # Use psycopg2 to execute queries
        with redshift_connection.cursor() as cursor:
            # Your SQL queries go here
            cursor.execute(query)

            # Fetch and print results
            headers = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            print("Retrieve Data successfully")

        # Close the connection
        redshift_connection.close()

        return results, headers

    """
     A method which queries given table and return response from DB
    Throws an exception when table or resource not found
    Handles client format, not resource
    """

    @staticmethod
    def get_dynamo_db_record(client, table_name: str, keys_values_to_search: object):
        try:
            response = client.get_item(TableName=table_name, Key=keys_values_to_search)
            return response["Item"]
        except Exception as e:
            print("Exception while reading record from dynamo db: ", e)

    """
    A method which supports reading data in batch
    Handles client format, not resource
    """

    @staticmethod
    def get_dynamo_db_data_in_batch(client, requested_item: object):
        try:
            response = client.batch_get_item(RequestItems=requested_item)
            return response
        except Exception as e:
            print("Exception while reading batch records from dynamo db: ", e)

    """
    A method which supports adding entry into the given dynamoDB table
    Handles client format, not resource
    """

    @staticmethod
    def add_dynamo_db_entry(client, table_name: str, record_to_insert: object):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
        try:
            response = client.put_item(TableName=table_name, Item=record_to_insert)
            return response["Attributes"]
        except Exception as e:
            print("Exception while adding an entry into dynamo db: ", e)

    """
    A method which supports removes entry from the given dynamoDB table
    Handles client format, not resource
    """

    @staticmethod
    def delete_dynamo_db_entry(client, table_name: str, record_to_delete: object):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
        try:
            response = client.delete_item(TableName=table_name, Key=record_to_delete)
            return response["Attributes"]
        except Exception as e:
            print("Exception while deleting records from dynamo db: ", e)

    """
    Query existing record using source and feed_name(including version)
    And inserts into Ingestion_Registry table
    """

    @staticmethod
    def insert_qa_entry_into_dynamo_db(client, table_name, feed_source, feed_name):
        key = {
            "source": {"S": feed_source},
            "feed_version": {"S": feed_name},
        }
        existing_record = AWSClientUtilities.get_dynamo_db_record(
            client, table_name, key
        )
        feed_qa_version_list = existing_record["feed_version"]["S"].split("|")
        existing_record["feed_version"] = {
            "S": rf"{feed_qa_version_list[0]}_qa|{feed_qa_version_list[1]}"
        }
        print(existing_record)
        insert_status = AWSClientUtilities.add_dynamo_db_entry(
            client, table_name, existing_record
        )
        print(insert_status)
