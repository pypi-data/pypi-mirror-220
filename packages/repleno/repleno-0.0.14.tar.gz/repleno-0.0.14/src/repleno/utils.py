from typing import List, Dict, Union
from datetime import timedelta
import math
import warnings
from difflib import SequenceMatcher
import csv
import os
import hashlib
import json


def remove_business_days(from_date, days_to_remove):
    """Removes a number of days from a date by skipping weeekends"""

    # TODO: be able to add holiday calendar to skip custom days

    if days_to_remove < 0:
        raise ValueError("Days to remove arg must be positive")

    days_to_remove_copy = days_to_remove
    current_date = from_date

    while days_to_remove_copy > 0:
        current_date += timedelta(days=-1)

        if current_date.weekday() >= 5:  # saturday = 6, sunday = 7
            continue
        else:
            days_to_remove_copy -= 1

    return current_date


def extract_and_transform_data(
    data: Union[str, List[Dict]],
    mandatory_keys: List[str],
    optional_keys: List[str] = None,
    mapping=None,
) -> List[Dict]:
    # Validate mapping keys
    if mapping:
        for mkey in mapping.keys():
            if mkey not in mandatory_keys and mkey not in optional_keys:
                raise KeyError(
                    f"Bad mapping keys: mapping keys must be the following: {mandatory_keys + optional_keys}"
                )

    # for CSV (it's assumed the str is a filename)
    if isinstance(data, str):
        if mapping:
            return read_and_parse_csv(data, mandatory_mapping=mapping)
        else:
            mandatory_mapping = {key: key for key in mandatory_keys}
            optional_mapping = None
            if optional_keys:
                optional_mapping = {key: key for key in optional_keys}

            return read_and_parse_csv(data, mandatory_mapping, optional_mapping)

    # for list of dicts
    if isinstance(data, list):
        if mapping:
            output = []
            for records in data:
                output.append(parse_dict(records, mapping))

            return output
        else:
            output = []
            mandatory_mapping = {key: key for key in mandatory_keys}
            optional_mapping = None
            if optional_keys:
                optional_mapping = {key: key for key in optional_keys}
            for records in data:
                output.append(parse_dict(records, mandatory_mapping, optional_mapping))

            return output

    raise TypeError(
        f"Bad data type: data must be either a CSV filename or a list of dicts, not a '{type(data)}'"
    )


def read_and_parse_csv(file, mandatory_mapping, optional_mapping={}) -> List[Dict]:
    # docu: mappings are key-value pairs where the key are the column that
    # should be in the output dictionary and the value is the key used to find
    # the data in the csv

    output = []
    try:
        with open(file, newline="", encoding="utf-8") as file:
            data = csv.DictReader(file)

            for row in data:
                output.append(parse_dict(row, mandatory_mapping, optional_mapping))

    except FileNotFoundError:
        print("Error: File not found.")
        raise
    except PermissionError:
        print("Error: Permission denied.")
        raise
    except csv.Error as e:
        print(f"Error: {e}")
        raise

    return output


def parse_dict(row, mandatory_mapping, optional_mapping={}):
    try:
        selected_row = {}

        if optional_mapping:
            for desired_key, file_key in optional_mapping.items():
                if file_key in row:
                    selected_row[desired_key] = row[file_key]

        # Raise an error if a mandatory key is not found
        for desired_key, file_key in mandatory_mapping.items():
            if file_key not in row:
                raise KeyError(f"Bad column/key: '{str(file_key)}' not found. Available ones: {row.keys()}")

            selected_row[desired_key] = row[file_key]

        return selected_row
    except ValueError:
        print(f"Bad row: {row}")
        raise


def get_value_index_pairs(pairs, target_values, optional_target_values=[]):
    """
    The user gives a series of index-value pairs, select some values and the
    function returns these selected values along with their index

    """
    result_values = []
    result_pairs = []

    for col in target_values:
        try:
            result_pairs.append(pairs.index(col))
            result_values.append(col)
        except ValueError:
            raise ValueError(get_not_found_column_message(col, pairs))

    for col in optional_target_values:
        try:
            result_pairs.append(pairs.index(col))
            result_values.append(col)
        except ValueError:
            warnings.warn(get_not_found_column_message(col, pairs))

    return result_values, result_pairs


def get_not_found_column_message(col, file_columns):
    similar_word = find_similar(col, file_columns)

    if similar_word:
        similar_word_str = f"A similar one found in the file is '{similar_word}'."
    else:
        similar_word_str = ""

    return f"Default column '{col}' not found. {similar_word_str}"


def find_similar(value, possible_values):
    suggested_word = ""
    suggested_word_ratio = 0

    for possible_val in possible_values:
        pval_ratio = SequenceMatcher(a=value, b=possible_val).ratio()

        if pval_ratio > suggested_word_ratio and (0.6 < pval_ratio < 1.0):
            suggested_word = possible_val
            suggested_word_ratio = pval_ratio

    return suggested_word


def to_csv(dictionaries, file_path: str, date_keys: list = None):
    """Print data in a csv file"""

    if not is_valid_dir(file_path):
        raise NotADirectoryError("Directory does not exist: ", file_path)

    if not is_valid_csv(file_path):
        raise AttributeError("Path must have csv extension: ", file_path)

    fieldnames = dictionaries[0].keys()

    separator = "\t"
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        file.write(f"sep={separator}\n")

        writer = csv.DictWriter(file, delimiter=separator, fieldnames=fieldnames)

        writer.writeheader()

        for row in dictionaries:
            if date_keys:
                for key in date_keys:
                    row[key] = row[key].strftime("%Y-%m-%d")
            writer.writerow(row)


def is_valid_dir(path):
    # remove the base name, if any
    only_path = os.path.split(path)[0]
    print(only_path)
    return os.path.exists(only_path)


def is_valid_csv(path):
    file_name = os.path.basename(path)
    return file_name.endswith(".csv")


def convert_to_int(input, item_code: str):
    try:
        return int(input)
    except ValueError:
        print(f"{input} connot be converted to an integer for item code {item_code}.")
        raise


def convert_to_float(input):
    try:
        if not input:
            return 1

        return float(input)
    except ValueError:
        print(f"{input} could not be converted into a float number.")
        raise

def hash_dicts_list(list_dict):
    result_json = json.dumps(list_dict, sort_keys=True)

    return hashlib.sha3_256(result_json.encode()).hexdigest()


def _get_key(dict, value):
    keys = []
    for key, val in dict.items():
        if val == value:
            keys.append(key)
    return keys


def _rename_keys(data, mandatory_mapping, optional_mapping):
    """
    Rename the keys of each dictionary in the list according to the provided mapping.

    Args:
        data (list): A list of dictionaries.
        mandatory_mapping (dict): A dictionary mapping the mandatory keys.
        optional_mapping (dict): A dictionary mapping the optional keys.

    Returns:
        A list of dictionaries with the renamed keys.
    """
    renamed_data = []
    for item in data:
        renamed_item = {}
        for key, value in item.items():
            if key in mandatory_mapping:
                renamed_item[mandatory_mapping[key]] = value
            elif key in optional_mapping:
                renamed_item[optional_mapping[key]] = value
        renamed_data.append(renamed_item)
    return renamed_data


def are_both_list_of_dicts_equal(list1, list2):
    """
    Checks whether two input lists contain identical dictionaries with the same
    frequencies, accounting for duplicates in the lists. This function does not
    support nested dictionaries.

    Args:
        list1 (list[dict]): First list of dictionaries
        list2 (list[dict]): Second list of dictionaries

    Returns:
        bool: True if both lists contain the same dictionaries. False
        otherwise.
    """

    if len(list1) != len(list2):
        return False

    dict_count_pairs_1 = get_dict_frequency(list1)
    dict_count_pairs_2 = get_dict_frequency(list2)

    # dicts are equal when their keys and values are the same.
    # As a reminder: dicts are a unordered collection of values.
    return True if dict_count_pairs_1 == dict_count_pairs_2 else False


def get_dict_frequency(list):
    """
    Returns a dictionary where the keys are the elements in the input list
    of dictionaries and the values are their frequencies.
    """
    result = {}
    for i in list:
        dict_key = tuple(sorted(i.items()))
        result.setdefault(dict_key, 0)
        result[dict_key] += 1

    return result
