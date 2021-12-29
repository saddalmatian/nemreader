import os
import boto3
import csv
from os import path
# Prefix file when split into multiple files
PREFIX_FILE = "NEM12#Split#"
# Quantity of files after splited
FILE_QUANTITY = 0


def max_line_file(file_path: str) -> int:
    """ Get max line of file
    :param file_path: the path of file
    :returns: max line of file
    """
    max_line = 0
    with open(file_path, 'r') as data_file:
        for line in data_file:
            max_line += 1
    return max_line


def split_nem12_file(file_path: str, line_quantity: int):
    """ Split the file into multiple files with given line quantity
    :param file_path: the path of file
    :param line_quantity: the line quantity you want to split for small files
    """
    global FILE_QUANTITY
    max_line = max_line_file(file_path)
    count = 0
    line_container = []
    number_id = 1
    current_line = 0
    with open(file_path, 'r') as data_file:
        for line in data_file:
            current_line += 1
            count += 1
            line_container.append(list(line.rstrip("\n").split(",")))
            if(count > line_quantity and
               list(line.split(","))[0] != "200"
               or current_line == max_line):
                with open('/tmp/split/' +
                          PREFIX_FILE +
                          str(number_id)+".csv", mode='w') as file:
                    nem_writer = csv.writer(
                        file, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
                    for record in line_container:
                        nem_writer.writerow(record)
                count = 0
                number_id += 1
                FILE_QUANTITY = number_id-1
                line_container = []


def lambda_handler(event, context):
    print(event)
    s3 = boto3.resource("s3")
    # Get bucket and key
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    # Make necessary folder
    if not path.isdir('tmp/original'):
        os.mkdir('/tmp/original')
    if not path.isdir('tmp/split'):
        os.mkdir('/tmp/split')
    # Download file uploaded
    s3.meta.client.download_file(bucket, key, '/tmp/'+key)
    # Start split file
    file_path = '/tmp/'+key
    split_nem12_file(file_path, 500)
    # Upload splitted files to s3
    for file in os.listdir('/tmp/split'):
        s3.meta.client.upload_file(
            '/tmp/split/'+file, bucket, 'split/'+str(FILE_QUANTITY)+"#"+file)
