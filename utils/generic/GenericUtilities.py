import re
import numpy
import pandas as pd


class GenericUtilities:
    """
    Method to sort list of dict based on key name. Supports both asc and desc. Default set to asc
    """
    @staticmethod
    def sort_list_of_dictionaries(list_of_dict: list, key_to_sort: any, reverse=False):
        if len(list_of_dict) == 0:
            print("Invalid input, list is empty")
            return
        if key_to_sort not in list_of_dict[0]:
            print("Key " + key_to_sort + " does not exists in the object")
            return
        return sorted(list_of_dict, key=lambda x: x[key_to_sort], reverse=reverse)

    """
    Method to get all partially matching objects (by particular key) from list of objects
    """

    @staticmethod
    def filter_partially_matched_records_from_list_of_objects(
        list, key_to_match, value_to_match
    ):
        if len(list) == 0:
            print("Invalid input, list is empty")
            return
        if key_to_match not in list[0]:
            print("Key " + key_to_match + " does not exists in the object")
            return
        return [obj1 for obj1 in list if value_to_match in obj1[key_to_match]]

    """
    Method to get all partially matching String from the list
    """

    @staticmethod
    def filter_partially_matched_records_from_list(list: list, value_to_match: any):
        if len(list) == 0:
            print("Invalid input, list is empty")
            return
        return [obj1 for obj1 in list if value_to_match in obj1[value_to_match]]

    """
    Method to get all partially matching String from the list
    """

    @staticmethod
    def filter_fully_matched_records_from_list(list: list, value_to_match: any):
        if len(list) == 0:
            print("Invalid input, list is empty")
            return
        return [obj1 for obj1 in list if value_to_match == obj1[value_to_match]]

    """
    Method to get all fully matching objects (based on particular key) from list of objects
    """

    def filter_matched_records_from_list_of_objects(
        list: list, key_to_match: any, value_to_match: any
    ):
        if len(list) == 0:
            print("Invalid input, list is empty")
            return
        if key_to_match not in list[0]:
            print("Key " + key_to_match + " does not exists in the object")
            return
        return [obj1 for obj1 in list if value_to_match == obj1[key_to_match]]

    """
    Checks the actual file name matches with the given expected file details
    """

    @staticmethod
    def is_file_name_matched(
        actual_file_name: str,
        file_name_initial: str,
        time_format: str,
        file_extension: str,
        object_initial_name="",
        shardnum="",
    ):
        file_name = (
            (object_initial_name if object_initial_name != "" else "")
            + file_name_initial
            + r"{}".format(time_format)
            + (shardnum if shardnum != "" else "")
            + "."
            + file_extension
        )
        print("Expected File name: " + file_name)
        print("Actual File Name: " + actual_file_name)
        return re.match(file_name, actual_file_name)

    @staticmethod
    def verify_count(parquet_file_path):
        df = pd.read_parquet(parquet_file_path)
        count_rows, count_columns = df.shape
        return count_rows, count_columns

    @staticmethod
    def verify_headers(parquet_file_path):
        df = pd.read_parquet(parquet_file_path)
        # expected_headers = [header.lower() for header in expected_headers]
        headers = df.columns.tolist()
        return headers

    @staticmethod
    def verify_key(parquet_file_path, key_columns):
        df = pd.read_parquet(parquet_file_path)
        print(df.columns.tolist())

        key_columns = [header.lower() for header in key_columns]
        # Check if all specified key columns exist in the DataFrame
        missing_columns = [col for col in key_columns if col not in df.columns]
        if missing_columns:
            raise KeyError(
                f"The following key columns are missing in the DataFrame: {missing_columns}"
            )

        return not df[key_columns].duplicated().any()

    @staticmethod
    def is_pgp_encrypted(file_path):
        with open(file_path, "rb") as file:
            header = file.read(6)
            return header.startswith(b"\x95\x01\x02")

    @staticmethod
    def convert_redshift_data_into_list_of_objects(columns, values):
        final_list = []
        for value in values:
            local_obj = {}
            for col_index in range(len(columns)):
                column = (
                    columns[col_index]
                    if "_stdz" not in columns[col_index]
                    else columns[col_index].replace("_stdz", "")
                )
                local_obj[column] = (
                    ""
                    if value[col_index] is None
                    or value[col_index] is pd.NaT
                    or value[col_index] is numpy.nan
                    else str(value[col_index])
                )
            final_list.append(local_obj)
        return final_list
