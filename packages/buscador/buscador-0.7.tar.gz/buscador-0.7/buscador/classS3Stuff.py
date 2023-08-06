import boto3
import json
import pandas as pd
from botocore.exceptions import ClientError
from io import StringIO


class S3Stuff:
    def __init__():
        pass

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
