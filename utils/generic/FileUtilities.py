import os
import json
import yaml
import gzip
import pathlib
import shutil
import pandas as pd
import numpy
import re
import fnmatch
import zipfile
import csv
from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import jsonlines


class FileUtilities:
    """File with opne() modes it supports
    'r' for read mode (default)
    'w' for write mode
    'a' for append mode
    'rb', 'wb', 'ab' for reading, writing, and appending binary files
    'r+', 'w+', 'a+' for reading and writing text files
    'rb+', 'wb+', 'ab+' for reading and writing binary files
    """

    """
    absolute_path: the path of the directory. It includes parent and child directories too
        For ex: parent
                parent/child
    """

    @staticmethod
    def create_directory(absolute_path: str):
        path = os.path.join(os.getcwd(), absolute_path)
        print("Creating directory: ", path)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    """
    absolute_path: the path of the directory
    This method deletes the directory and all its content. Be mindful while using the method
    """

    @staticmethod
    def delete_directory(absolute_path: str):
        path = os.path.join(os.getcwd(), absolute_path)
        print("Removing directory: ", path)
        shutil.rmtree(path, ignore_errors=True)

    """
    file_directory: must be dir1/child_dir/child_dir2 format
    file_name: The name of the which you would like to delete with extension
    """

    @staticmethod
    def delete_file_from_path(file_name: str, file_directory=""):
        path = os.path.join(os.getcwd(), file_directory, file_name)
        print("Removing File: ", path)
        try:
            pathlib.Path.unlink(path)
        except:
            print("File not found in the given path")

    """
    #suppourts files with extension xls, xlsx
    file_directory: The directory where file exists
    file_name: The excel file name with extension
    sheet_name: The sheet in excel which we would like to read
    """

    @staticmethod
    def read_excel_file_content(file_name: str, sheet_name: str, file_directory=""):
        path = os.path.join(os.getcwd(), file_directory, file_name)
        print("Reading excel file: ", path)
        try:
            data_feed = pd.read_excel(path, sheet_name=sheet_name)
            return data_feed
        except Exception as e:
            print("Exception/Error while reading excel file: ", e)

    """
    #supports files with extension dat, csv.
    file_directory: The directory where file exists
    file_name: The excel file name with extension
    separator: by which we should separate data
    
    Pass | for dat files and , for csv files
    """

    @staticmethod
    def read_dat_csv_file_content(
            file_name, separator=",", file_directory="", encoding="utf-8"
    ):
        # ISO-8859-1
        path = os.path.join(os.getcwd(), file_directory, file_name)
        print("Reading csv file: ", path)
        try:
            data_feed = pd.read_csv(path, encoding=encoding, sep=separator)
            data_feed = data_feed.replace(numpy.nan, "", regex=True)
            # print(data_feed.columns)
            return data_feed
        except Exception as e:
            print("Exception/Error while reading csv file: ", e)

    """
    #supports files with extension json.
    file_directory: The directory where file exists
    file_name: The json file name with extension
    separator: by which we should separate data
    """

    @staticmethod
    def read_json_file_content(file_name: str, file_directory=""):
        path = os.path.join(os.getcwd(), file_directory, file_name)
        print("Reading json file: ", path)
        try:
            with open(path) as json_data:
                content = json.load(json_data)
                return content
        except Exception as e:
            print("Exception/Error while reading json file: ", e)

    """
    Method to read jsonl (which is a text file type) and txt files 
    """

    @staticmethod
    def read_file(txt_file_name: str, file_directory=""):
        path = os.path.join(os.getcwd(), file_directory, txt_file_name)
        try:
            with open(path, "r") as file:
                return file.read()
        except Exception as e:
            print("Exception occurred while reading zip file: ", e)

    @staticmethod
    def read_xml_file_content(file_name: str, file_directory=""):
        print()

    @staticmethod
    def convert_xml_to_json(xml_file_name: str, file_directory=""):
        print()

    @staticmethod
    def convert_json_to_xml(json_file_name: str, file_directory=""):
        print()

    """
    #Method which reads yaml file and return the dictionary kind of object
    file_directory: the directory where yaml file exists. If its a root directory of the project, pass ''
    """

    @staticmethod
    def read_yaml_file_content(yaml_file_name: str, file_directory=""):
        path = os.path.join(os.getcwd(), file_directory, yaml_file_name)
        print("Reading yml file: ", path)
        try:
            with open(path, "r") as file:
                base_data = yaml.safe_load(file)
                return base_data
        except Exception as e:
            print("Exception/Error while reading yaml file: ", e)

    """
    Method which reads parquet file and returns data feed
    """

    @staticmethod
    def read_parquet_file_content(
            parquet_file_name: str, file_directory="", columns=[]
    ):
        path = os.path.join(os.getcwd(), file_directory, parquet_file_name)
        print("Reading parquet file: ", path)
        try:
            if len(columns) == 0:
                return pd.read_parquet(path, engine="fastparquet")
            else:
                return pd.read_parquet(path, engine="fastparquet", columns=columns)
            # we can pass columns=[name of columsn] list as one param to read only those columns data
        except Exception as e:
            print("Exception/Error while reading parquet file: ", e)

    """
    Method which zips a unzip file. Both the files will be placed in same directory as we are taking only one file_directory
    """

    @staticmethod
    def zip_file(input_file_name: str, output_file_name: str, file_directory=""):
        original = os.path.join(os.getcwd(), file_directory, input_file_name)
        compressed = os.path.join(os.getcwd(), file_directory, output_file_name)
        print("Compressing file from: " + original + " to " + compressed)
        try:
            with open(original, "rb") as f_in:
                with gzip.open(compressed, "wb") as f_out:
                    f_out.writelines(f_in)
        except Exception as e:
            print("Exception/Error while zipping file: ", e)
        return output_file_name

    """
    Method which unzips a zip file. Both the files will be placed in same directory as we are taking only one file_directory
    """

    @staticmethod
    def unzip_file(zip_file_name: str, unzip_file_name: str, file_directory=""):
        original = os.path.join(os.getcwd(), file_directory, zip_file_name)
        unzipped = os.path.join(os.getcwd(), file_directory, unzip_file_name)
        try:
            with gzip.open(original, "rb") as f_in:
                with open(unzipped, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print("File is uncompressed.")
        except Exception as e:
            print("Exception/Error while unzipping file: ", e)

        return unzip_file_name

    """
    Method to get duplicate records from the given zip file
    """

    @staticmethod
    def get_duplicate_records_from_zip_file(zip_file_name: str, file_directory=""):
        unique_records = set()
        duplicate_records = []
        file = FileUtilities.read_zip_file(file_directory, zip_file_name)
        for line in file:
            line = line.strip()
            if line in unique_records:
                duplicate_records.append(line)
            else:
                unique_records.add(line)
        return duplicate_records

    """
    Method to get duplicate records from the unzipped file
    """

    @staticmethod
    def get_duplicate_records_from_file(file_name: str, file_directory=""):
        unique_records = set()
        duplicate_records = []
        file = FileUtilities.read_file(file_directory, file_name)
        for line in file:
            line = line.strip()

            if line in unique_records:
                duplicate_records.append(line)
            else:
                unique_records.add(line)
        return duplicate_records

    """
    Method to check given file is empty or not
    """

    @staticmethod
    def is_file_empty(file_name: str, file_directory=""):
        path = os.path.join(os.getcwd(), file_directory, file_name)
        return os.stat(path).st_size == 0

    """
    Method to check given zip file is empty or not
    """

    @staticmethod
    def is_zip_file_empty(zip_file_name: str, file_directory=""):
        file = FileUtilities.read_zip_file_get_list_of_objects(
            zip_file_name, file_directory=file_directory
        )
        records = []
        for line in file:
            records.append(line)
        return len(records) == 0

    """
    Method to return the size of the file
    """

    @staticmethod
    def get_file_size(zip_file_name: str, file_directory=""):
        file_path = os.path.join(os.getcwd(), file_directory, zip_file_name)
        return os.path.getsize(file_path)

    """
    Supports Excel, dat, csv, jsonl, parquet files and returns list of dictionaries
    Also handles validation of both columns and values are same in number as its index based
    """

    @staticmethod
    def read_file_data_into_list_of_objects(
            file_name: str,
            file_type: str,
            file_directory="",
            sheet_name="Sheet1",
            separator="~",
            columns=[],
    ):
        list_data = []
        try:
            data = ""
            if file_type == "xlsx":
                data = FileUtilities.read_excel_file_content(
                    file_name + "." + file_type, sheet_name, file_directory
                )
            elif file_type == "csv" or file_type == "dat":
                data = FileUtilities.read_dat_csv_file_content(
                    file_name + "." + file_type,
                    separator=separator,
                    file_directory=file_directory,
                )
            elif file_type == "jsonl":
                data = FileUtilities.read_file(
                    file_name + "." + file_type, file_directory
                )
                data = data.split(
                    "\n"
                )  # Splitting based on new line as jsonl is a format of JSON Lines separated by new line
                actual = []
                for row in data:
                    if row:
                        actual.append(json.loads(row))
                        # keys = list(data_dict.keys())
                # print("keys of dictionary:", keys)
                return actual
            elif file_type == "parquet":
                data = FileUtilities.read_parquet_file_content(
                    file_name + "." + file_type,
                    file_directory=file_directory,
                    columns=columns,
                )
            headers = data.columns
            # print(headers)
            for index in range(len(data.values)):
                value_row = data.values[index]
                value = {}
                for lower_index in range(len(headers)):
                    value[headers[lower_index]] = (
                        value_row[lower_index]
                        if value_row[lower_index] is not numpy.nan
                           and value_row[lower_index] is not None
                        else ""
                    )
                # print(value)
                list_data.append(value)
            return list_data
        except Exception as e:
            print("Exception occurred while reading file: ", e)

    """
    Supports xlsx, csv, dat files and returns header names in the given file as List
    """

    @staticmethod
    def get_headers_of_file(
            file_name: str,
            file_type: str,
            file_directory="",
            sheet_name="Sheet1",
            separator="|",
            columns=[],
    ):
        try:
            data = ""
            if file_type == "xlsx":
                data = FileUtilities.read_excel_file_content(
                    file_name + "." + file_type, sheet_name, file_directory
                )
            elif file_type == "csv" or file_type == "dat":
                data = FileUtilities.read_dat_csv_file_content(
                    file_name + "." + file_type,
                    separator=separator,
                    file_directory=file_directory,
                )
            elif file_type == "parquet":
                data = FileUtilities.read_parquet_file_content(
                    file_name + "." + file_type,
                    file_directory=file_directory,
                    columns=columns,
                )
            return data.columns
        except Exception as e:
            print("Exception occurred while reading file: ", e)

    """
    Handles the files of dat.gz, jsonl.gz and returns list of dictionaries
    Also handles validation of both columns and values are same in number as its index based
    """

    @staticmethod
    def read_zip_file_get_list_of_objects(
            zip_file_name: str, file_directory="", separator="|"
    ):
        path = os.path.join(os.getcwd(), file_directory, zip_file_name)
        try:
            data = []
            if ".csv.gz":
                with gzip.open(path, "rt") as fin:
                    for line in fin:
                        data.append(line)
            else:
                with gzip.open(path, "rb") as fin:
                    for line in fin:
                        data.append(line)

            final_list = []
            if ".dat.gz" in zip_file_name or ".csv.gz" in zip_file_name:
                columns = data[0].decode("utf-8").split(separator)
                print("Inside method columns:", columns)
                for index in range(1, len(data)):
                    obje = {}
                    values = data[index].decode("utf-8").split(separator)
                    for local_index in range(len(values)):
                        if (local_index + 1) != len(values):
                            obje[re.sub('"', "", columns[local_index])] = re.sub(
                                '"', "", values[local_index]
                            )
                        else:
                            key = re.sub(
                                '"',
                                "",
                                re.sub(
                                    "\\n",
                                    "",
                                    re.sub("\\r", "", columns[local_index]),
                                ),
                            )
                            local_value = re.sub(
                                "\\n",
                                "",
                                re.sub('"', "", re.sub("\\r", "", values[local_index])),
                            )
                            obje[key] = local_value
                    # print(obje)
                    # print(len(final_list))
                    final_list.append(obje)
                # print(len(final_list))
                return final_list
            elif (
                    ".jsonl.gz" in zip_file_name
            ):  # file name should include .jsonl.gz to recognize
                for row in data:
                    final_list.append(json.loads(row.decode("utf-8")))
                return final_list
            elif ".csv.gz" in zip_file_name:
                val = re.sub("\\n", "", re.sub('"', "", re.sub("\\r", "", data[0])))
                columns = re.split(r"[~|]", val)
                # print(columns)
                for index in range(1, len(data)):
                    obje = {}
                    # values = data[index].decode("utf-8").split("~")
                    data1 = re.sub('"', "", data[index])
                    values = re.split(r"[~|]", data1)
                    for local_index in range(len(values)):
                        if (local_index + 1) != len(values):
                            obje[re.sub('"', "", columns[local_index])] = re.sub(
                                '"', "", values[local_index]
                            )
                        else:
                            key = re.sub('"', "", columns[local_index])
                            key = re.sub("\\n", "", key)
                            local_value = re.sub("\\n", "", values[local_index])
                            local_value = re.sub('"', "", local_value)
                            obje[key] = local_value
                    final_list.append(obje)
                return final_list
        except Exception as e:
            print("Exception occurred while reading zip file: ", e)

    """
    Supports zip file of dat and excel. For ex: .dat.gz etc
    Returns all column names in list
    """

    @staticmethod
    def read_zip_file_get_headers_as_list(
            zip_file_name: str, file_directory="", separator="|"
    ):
        path = os.path.join(os.getcwd(), file_directory, zip_file_name)
        try:
            data = []
            with gzip.open(path, "r") as fin:
                for line in fin:
                    data.append(line)
            if ".dat.gz" in zip_file_name:
                columns = re.sub(
                    "\\n",
                    "",
                    re.sub('"', "", re.sub("\\r", "", data[0].decode("utf-8"))),
                ).split(separator)
                return columns
            elif ".csv.gz" in zip_file_name:
                data = re.sub(
                    "\\n",
                    "",
                    re.sub('"', "", re.sub("\\r", "", data[0].decode("utf-8"))),
                )
                columns = re.split(r"[~|]", data)
                # column delimiters for fantasy are ~ and |
                return columns
        except Exception as e:
            print("Exception occurred while reading zip file: ", e)

    """
    Renames the file and place it in target directory
    """

    @staticmethod
    def rename_file(
            old_file_name: str, new_file_name: str, old_file_dir="", new_file_dir=""
    ):
        old_file = os.path.join(old_file_dir, old_file_name)
        new_file = os.path.join(new_file_dir, new_file_name)
        try:
            os.rename(old_file, new_file)
        except Exception as e:
            print("Exception occured while renaming file: ", e)

    """
    returns list of all matching files from the given directory
    """

    @staticmethod
    def list_all_macthing_files(pattern: str, file_directory="."):
        print("Checking mathing files")
        try:
            return fnmatch.filter(
                os.listdir(os.path.join(os.getcwd(), file_directory)), pattern
            )
        except Exception as e:
            print("Exception while getting all matching files: ", e)

    """
    Method which writes list<dict> object into an csv file.
    file_name: The name of the file with .csv as extension
    data: list of dictionaries
    file_directory: In which directory the csv file should save
    """

    @staticmethod
    def write_into_csv(file_name: str, data: list, file_directory=""):
        path = os.path.join(os.getcwd(), file_directory, file_name)
        keys = data[0].keys()
        with open(path, "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    """
    Method to convert csv file into parquet file
    csv_file_name: name of csv file with .csv as extension
    parquet_file_name: name of parquet file with .parquet as extension
    file_directory: In which directory the file read and write
    """

    @staticmethod
    def convert_csv_to_parquet(
            csv_file_name: str, parquet_file_name: str, file_directory=""
    ):
        csv_path = os.path.join(os.getcwd(), file_directory, csv_file_name)
        parquet_path = os.path.join(os.getcwd(), file_directory, parquet_file_name)
        df = pd.read_csv(csv_path)
        df.to_parquet(parquet_path)

    """
    convert files with .avro extension to jsonl
    file_directory: The directory where file exists
    file_name: The avro file name with extension
    """

    @staticmethod
    def convert_avro_to_jsonl(output_file, file_name, file_directory="", zone=""):
        try:
            path = os.path.join(os.getcwd(), file_directory, file_name)
            print("Converting avro to jsonl", path)

            with open(path, "rb") as f:
                reader = DataFileReader(f, DatumReader())
                records = [record for record in reader]
                reader.close()

            # Convert avro records to json
            json_records = [json.dumps(record) for record in records]

            # Write JSON data to a file
            if zone == "landed":
                json_output_path = "test_data\seatgeek\landed_output.json"
            # elif zone == "processed":
            else:
                json_output_path = "test_data\seatgeek\processed_output.json"
            with open(json_output_path, "w") as json_file:
                for json_record in json_records:
                    json_file.write(json_record + "\n")

            # Convert json to json lines
            if zone == "landed":
                jsonl_output_path = "test_data\seatgeek\landed_output.jsonl"
            # elif zone == "processed":
            else:
                jsonl_output_path = "test_data\seatgeek\processed_output.jsonl"
            # jsonl_output_path = 'test_data\seatgeek\output.jsonl'
            with open(json_output_path, "r") as json_file, open(
                    jsonl_output_path, "w"
            ) as jsonl_file:
                for line in json_file:
                    data = json.loads(line.strip())
                    jsonl_file.write(json.dumps(data) + "\n")

            print(f"Conversion completed. Output written to {jsonl_output_path}")
            return jsonl_output_path

        except Exception as e:
            print("Exception/Error while converting avro file: ", e)
            return None

    """
    Writes avro file content into target_file_name which expects .json in name
    """

    @staticmethod
    def write_avro_into_json(file_name, target_file_name, file_directory=""):
        try:
            path = os.path.join(os.getcwd(), file_directory, file_name)
            print("Converting avro to json", path)
            with open(path, "rb") as f:
                reader = DataFileReader(f, DatumReader())
                records = [record for record in reader]
                reader.close()

            # Convert avro records to json
            json_records = [json.dumps(record) for record in records]
            print(len(json_records), "\n")
            print(json_records[0])
            target_path = os.path.join(os.getcwd(), file_directory, target_file_name)
            with open(target_path, "w") as json_file:
                # for json_record in json_records:
                json_file.write(str(json_records))

        except Exception as e:
            print("Exception/Error while converting avro file: ", e)
            return None

    @staticmethod
    def convert_avro_to_list_of_dicts(file_name, file_directory=""):
        """
        Reads avro file and returns list of dictionaries
        """
        try:
            path = os.path.join(os.getcwd(), file_directory, file_name)
            print("Converting avro to jsonl", path)

            with open(path, "rb") as f:
                reader = DataFileReader(f, DatumReader())
                records = [json.loads(json.dumps(record)) for record in reader]
                reader.close()
            print(records[0])
            json_list = []
            for record in records:
                main_keys = record.keys()
                obje = {}
                for key in main_keys:
                    obje[key.casefold()] = (
                        "" if record[key] is None else str(record[key])
                    )
                json_list.append(obje)
            return json_list

        except Exception as e:
            print("Exception/Error while converting avro file: ", e)
            return None

    """
    Method supports all files irrespective of compressed or not.
    It just need a file name which identies file type and its compression
    Reads the file content and returns list of objects
    """

    @staticmethod
    def read_file_into_list_of_objects(
            file_name: str,
            file_directory="",
            sheet_name="Sheet1",
            separator="|",
            columns=[],
    ):
        try:
            data = ""
            if "xlsx" in file_name:
                data = FileUtilities.read_excel_file_content(
                    file_name, sheet_name, file_directory
                )
            elif (
                    "csv" in file_name
                    and "csv." not in file_name
                    or "dat" in file_name
                    and "dat." not in file_name
            ):
                data = FileUtilities.read_dat_csv_file_content(
                    file_name,
                    separator=separator,
                    file_directory=file_directory,
                )
            elif "jsonl" in file_name and "jsonl." not in file_name:
                data = FileUtilities.read_file(file_name, file_directory)
                data = data.split(
                    "\n"
                )  # Splitting based on new line as jsonl is a format of JSON Lines separated by new line
                return [json.loads(row) for row in data]
            elif "json" in file_name and "jsonl" not in file_name:
                data = FileUtilities.read_json_file_content(file_name, file_directory)
                final_list = []
                for record in data:
                    local = {}
                    for key in record.keys():
                        local[key.casefold()] = (
                            "" if record[key] is None else str(record[key])
                        )
                    final_list.append(local)
                return final_list
            elif "yml" in file_name:
                data = FileUtilities.read_yaml_file_content(file_name, file_directory)
                return data
            elif "parquet" in file_name and "parquet." not in file_name:
                data = FileUtilities.read_parquet_file_content(
                    file_name,
                    file_directory=file_directory,
                    columns=columns,
                )
            elif ".dat.gz" in file_name or ".csv.gz" in file_name:
                data = []
                path = os.path.join(os.getcwd(), file_directory, file_name)
                with gzip.open(path, "rb") as fin:
                    for line in fin:
                        data.append(line)
                final_list = []
                columns = data[0].decode("utf-8").split(separator)
                # print("columns: ", len(columns), "\n")
                MATCHER = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
                for index in range(1, len(data)):
                    obje = {}
                    values = (
                        MATCHER.split(data[index].decode("utf-8"))
                        if ".csv.gz" in file_name and separator == ","
                        else data[index].decode("utf-8").split("|")
                    )
                    # print("values: ", len(values), "\n")
                    for local_index in range(len(values)):
                        if (local_index + 1) != len(values):
                            obje[re.sub('"', "", columns[local_index].casefold())] = (
                                re.sub('"', "", values[local_index])
                            )
                        else:
                            key = re.sub(
                                '"',
                                "",
                                re.sub(
                                    "\\n",
                                    "",
                                    re.sub("\\r", "", columns[local_index].casefold()),
                                ),
                            )
                            local_value = re.sub(
                                "\\n",
                                "",
                                re.sub('"', "", re.sub("\\r", "", values[local_index])),
                            )
                            obje[key] = local_value
                    # print(obje)
                    # print(len(final_list))
                    final_list.append(obje)
                # print(len(final_list))
                return final_list
            elif ".jsonl.gz" in file_name:
                path = os.path.join(os.getcwd(), file_directory, file_name)
                data = []
                with gzip.open(path, "rb") as fin:
                    for line in fin:
                        data.append(line)
                return [json.loads(row.decode("utf-8")) for row in data]
            elif ".avro" in file_name:
                # Converting avro to json file
                json_data = FileUtilities.convert_avro_to_list_of_dicts(
                    file_name, file_directory=file_directory
                )
                return json_data
            # Below code is only for xlsx, parquet, csv and dat files
            headers = data.columns
            # print(headers)
            list_data = []
            for data_value in data.values:
                # print("reading...", value_row)
                value = {}
                for lower_index in range(len(headers)):
                    value[headers[lower_index].casefold()] = (
                        str(data_value[lower_index])
                        if data_value[lower_index] is not numpy.nan
                           and data_value[lower_index] is not None
                           and data_value[lower_index] is not pd.NaT
                        else ""
                    )
                # print(value)
                list_data.append(value)
            return list_data
        except Exception as e:
            print("Exception occurred while reading file: ", e)

    """
    Supports xlsx, csv, dat files and returns header names in the given file as List
    """

    @staticmethod
    def read_feed_headers_as_list(
            file_name: str,
            file_directory="",
            sheet_name="Sheet1",
            separator="|",
            columns=[],
    ):
        try:
            data = ""
            if "xlsx" in file_name:
                data = FileUtilities.read_excel_file_content(
                    file_name, sheet_name, file_directory
                )
            elif "csv" in file_name or "dat" in file_name:
                data = FileUtilities.read_dat_csv_file_content(
                    file_name,
                    separator=separator,
                    file_directory=file_directory,
                )
            elif "parquet" in file_name:
                data = FileUtilities.read_parquet_file_content(
                    file_name,
                    file_directory=file_directory,
                    columns=columns,
                )
            elif "jsonl.gz" in file_name:
                data = FileUtilities.read_parquet_file_content(
                    file_name,
                    file_directory=file_directory,
                    columns=columns,
                )
            elif "dat.gz" in file_name or "csv.gz" in file_name:
                path = os.path.join(os.getcwd(), file_directory, file_name)
                data = []
                with gzip.open(path, "r") as fin:
                    for line in fin:
                        data.append(line)
                columns = re.sub(
                    "\\n",
                    "",
                    re.sub('"', "", re.sub("\\r", "", data[0].decode("utf-8"))),
                ).split(separator)
                for column in columns:
                    data.append(column)
                return data
            elif ".avro" in file_name:
                # Converting avro to json file
                json_array = FileUtilities.convert_avro_to_list_of_dicts(
                    file_name, file_directory=file_directory
                )
                if len(json_array) == 0:
                    print("No records found in avro file", "\n")
                    return None
                return [column for column in json_array[0].keys()]
            elif ".json" in file_name:
                json_content = FileUtilities.read_json_file_content(
                    file_name, file_directory
                )
                return FileUtilities.read_json_keys_values(json_content[0])
            return data.columns

        except Exception as e:
            print("Exception occurred while reading file: ", e)

    @staticmethod
    def copy_file(file_name: str, soruce_dir: str, target_dir: str):
        source = os.path.join(soruce_dir, file_name)
        target = os.path.join(target_dir, file_name)
        shutil.copy2(source, target)

    @staticmethod
    def get_primary_key_records_from_data(data, primary_key):
        list1 = list()
        for row in data:
            value = row[primary_key]
            list1.append(rf"'{value}'")
        return list1

    @staticmethod
    def read_json_keys_values(object, prev_key=None, keys=[]):
        if type(object) != type({}):
            keys.append(prev_key)
            return keys
        new_keys = []
        for k, v in object.items():
            if prev_key != None:
                new_key = "{}.{}".format(prev_key, k)
            else:
                new_key = k
            new_keys.extend(FileUtilities.read_json_keys_values(v, new_key, []))
        return new_keys
