import boto3
import json
import pandas as pd
from botocore.exceptions import ClientError
from io import StringIO


def write_json(data, bucket: str, key: str):
    """
    Write json to S3.
    Args:
        data (_type_): Data to be written
        bucket (str): Destination S3 bucket
        key (str): S3 object key

    Returns:
        str: Write success message
    """
    s3_resource = boto3.resource("s3")
    obj = s3_resource.Object(bucket, key)
    try:
        obj.put(Body=(bytes(json.dumps(data, indent=2).encode("UTF-8"))))
        del obj
        return f"Object '{key}' succesfully written to bucket '{bucket}'"
    except:
        raise Exception(f"Could not write object '{key}' to bucket '{bucket}'")


def read_json(bucket: str, key: str):
    """
    Read json from S3.
    Args:
        bucket (str): Source S3 bucket.
        key (str): Target S3 object key.

    Returns:
        dict: json as dict.
    """
    s3_resource = boto3.resource("s3")
    file = s3_resource.Object(bucket, key)
    file_contents = file.get()["Body"].read().decode("utf-8")

    return json.loads(file_contents)


def read_jsonl(bucket: str, key: str):
    """
    Read json from S3.
    Args:
        bucket (str): Source S3 bucket.
        key (str): Target S3 object key.

    Returns:
        dict: json as dict.
    """
    s3_resource = boto3.resource("s3")
    file = s3_resource.Object(bucket, key)
    file_contents = file.get()["Body"].read().decode("utf-8")
    json_lines = tuple(
        json_line for json_line in file_contents.splitlines() if json_line.strip()
    )
    json_objs = tuple(json.loads(json_line) for json_line in json_lines)
    json_objs = list(json_objs)
    return json_objs


def read_csv(bucket, key):
    """
    Args:
        Bucket (str): Bucket to read data from
        key (str): Object key

    Returns:
        DataFrame: Read data
    """
    s3_client = boto3.client("s3")

    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
    except ClientError as e:
        raise e

    df = pd.read_csv(obj["Body"])
    return df


def write_csv(bucket: str, key: str, df):
    """
    Args:
        Bucket (str): Bucket to write data to
        key (str): Object name
        df (DataFrame): Data to write

    Returns:
        str: Success message
    """
    s3_resource = boto3.resource("s3")
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    try:
        s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())
    except:
        raise Exception(f"Failed to write object '{key}' to bucket '{bucket}'")
    return f"Object '{key}' written to bucket '{bucket}'"


def find_keys_value(adict: dict, key: str):
    """Returns value of a given key, even if nested

    Args:
        adict (dict): target dictionary
        key (str): target dictionary key

    Returns:
        Value of target dictionary key
    """
    stack = [adict]
    while stack:
        d = stack.pop()
        if key in d:
            return d[key]
        for v in d.values():
            if isinstance(v, dict):
                stack.append(v)
            if isinstance(v, list):
                stack += v


def get_paths(my_dict: dict, path=None):
    """
    Get paths for nested keys in dictionaries.
    Args:
        my_dict (dict): Target dictionary.
        path (list, optional): Defaults to None.
    """
    if path is None:
        path = []
    for k, v in my_dict.items():
        newpath = path + [k]
        if isinstance(v, dict):
            for u in get_paths(v, newpath):
                yield u
        else:
            yield newpath, v
