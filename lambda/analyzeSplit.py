import json
import boto3
import os
from os import path
from nemreader import read_nem_file

# Prefix file when split into multiple files
PREFIX_FILE = "NEM12#Split#"
# Quantity of files after splited


def connect_readings(d1: dict, d2: dict):
    """ Connect 2 readings dicts together, d2 connect to d1
    :param d1: first dict
    :param d2: second dict
    """
    for nmi in d2:
        if nmi not in d1:
            d1[nmi] = {}
        for suffix in d2[nmi]:
            if suffix not in d1[nmi]:
                d1[nmi][suffix] = []
            for readings in d2[nmi][suffix]:
                d1[nmi].setdefault(suffix, []).append(readings)


def connect_transaction(d1: dict, d2: dict):
    """ Connect 2 transaction dicts together, d2 connect to d1
    :param d1: first dict
    :param d2: second dict
    """
    for nmi in d2:
        if nmi not in d1:
            d1[nmi] = {}
        for suffix in d2[nmi]:
            if suffix not in d1[nmi]:
                d1[nmi][suffix] = []
            for readings in d2[nmi][suffix]:
                d1[nmi].setdefault(suffix, []).append([])


def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    client = boto3.client("s3")
    # Get bucket and key
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    formatted_key = key.replace("%23", "#")
    # Get file order number
    order_number = int(key.replace(".csv", "").split("%23")[3])
    # Make necessary folder
    if not path.isdir('/tmp/split'):
        os.mkdir('/tmp/split')
    # Download file
    s3.meta.client.download_file(bucket, formatted_key, '/tmp/'+formatted_key)
    # Define data container to contain all the raw datas
    data_container = {}
    # Define max split file
    max_file = int(key.replace("split/", "").split("%23")[0])

    # Start analyze
    if(order_number == 1):
        # Start write raw data
        m = read_nem_file('/tmp/'+formatted_key,
                          quantity=order_number)
        contain_header = []
        for field in m.header:
            contain_header.append(str(field))
        # Import header into data_container
        data_container['header'] = contain_header
        # Link two readings and transactions into data_container
        data_container['readings'] = {}
        data_container['transactions'] = {}
        connect_readings(data_container['readings'], m.readings)
        connect_transaction(data_container['transactions'], m.transactions)
        # Write raw data to file
        raw_file_name = str(max_file)+"#NEM12#raw#"+str(order_number)
        f = open("/tmp/"+raw_file_name, 'w')
        f.write(json.dumps(data_container, default=str, indent=4))
        s3.meta.client.upload_file('/tmp/'+raw_file_name,
                                   bucket,
                                   'raw/'+raw_file_name+".csv")

    elif(order_number > 1 and order_number < max_file):
        # Start write raw data
        m = read_nem_file('/tmp/'+formatted_key,
                          quantity=order_number,
                          ignore_missing_header=True)
        # Link two readings and transactions into data_container
        data_container['readings'] = {}
        data_container['transactions'] = {}
        connect_readings(data_container['readings'], m.readings)
        connect_transaction(data_container['transactions'], m.transactions)
        # Write raw data to file
        raw_file_name = str(max_file)+"#NEM12#raw#"+str(order_number)
        f = open("/tmp/"+raw_file_name, 'w')
        f.write(json.dumps(data_container, default=str, indent=4))
        s3.meta.client.upload_file('/tmp/'+raw_file_name,
                                   bucket,
                                   'raw/'+raw_file_name+".csv")

    elif(order_number == max_file):
        response = client.list_objects_v2(
            Bucket=bucket,
            Prefix='raw/',
        )
        current_s3_objects = (response["KeyCount"])
        # while last file had not been uploaded to s3
        while(current_s3_objects != max_file-1):
            # Get current objects in s3
            response = client.list_objects_v2(
                Bucket=bucket,
                Prefix='raw/',
            )
            current_s3_objects = (response["KeyCount"])
            if(current_s3_objects == max_file-1):
                # lambda_invoke = boto3.client('lambda')

                # Start write raw data
                m = read_nem_file('/tmp/'+formatted_key,
                                  quantity=order_number,
                                  ignore_missing_header=True)
                data_container['readings'] = {}
                data_container['transactions'] = {}
                connect_readings(data_container['readings'], m.readings)
                connect_transaction(
                    data_container['transactions'], m.transactions)
                # Write raw data to file
                raw_file_name = str(max_file)+"#NEM12#raw#"+str(order_number)
                f = open("/tmp/"+raw_file_name, 'w')
                f.write(json.dumps(data_container, default=str, indent=4))
                s3.meta.client.upload_file(
                    '/tmp/'+raw_file_name,
                    bucket,
                    'raw/'+raw_file_name+".csv")
                client = boto3.client('lambda')
                client.invoke(
                    FunctionName='arn:aws:lambda:ap-southeast-1:769253686157:function:analyzeRaw',
                    InvocationType='RequestResponse',
                    Payload=json.dumps({"Bucket": bucket})
                )
