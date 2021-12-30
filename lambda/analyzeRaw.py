import datetime
import boto3
import json
import os
from os import path
from nemreader import nem_objects


def get_readings(data_list: list):
    """ Get Reading from a list, decrypted datetime object from str
    :returns: nem_objects.Reading
    """
    t_start = (convert_datetime(data_list[0]))
    t_end = (convert_datetime(data_list[1]))
    read_value = data_list[2],
    uom = data_list[3]
    meter_serial_number = data_list[4]
    quality_method = data_list[5]
    event_code = data_list[6]
    event_desc = data_list[7]
    val_start = data_list[8]
    val_end = data_list[9]
    return nem_objects.Reading(t_start, t_end, read_value, uom,
                               meter_serial_number, quality_method, event_code,
                               event_desc, val_start, val_end)


def connect_readings_formatted(d1: dict, d2: dict):
    """ Connect 2 readings dicts together, d2 connect to d1
    with date time decrypted
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
                d1[nmi].setdefault(suffix, []).append(get_readings(readings))


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


def convert_datetime(datetime_str: str):
    """ Convert datetime from string to datetime object
    :returns: datetime object
    """
    dt = datetime_str.replace('-', ' ').replace(':', ' ').split(' ')
    year = int(dt[0])
    month = int(dt[1])
    day = int(dt[2])
    hour = int(dt[3])
    minute = int(dt[4])
    second = int(dt[5])
    return datetime.datetime(year, month, day, hour, minute, second)


def lambda_handler(event, context):
    print("Before Export Result and Test for sure")
    # Get all raw file from s3
    client = boto3.client('s3')
    resource = boto3.resource('s3')
    bucket_name = event['Bucket']
    # Get bucket from event
    response = client.list_objects_v2(
        Bucket=bucket_name,
        Prefix='raw/',
    )
    bucket = resource.Bucket(bucket_name)
    # Create a container contains all raw data together
    raw_data_container = {}
    for item in response['Contents']:
        key = item['Key']
        if not path.isdir('/tmp/raw'):
            os.mkdir('/tmp/raw')
        # Download file
        bucket.download_file(key, '/tmp/'+key)
        f = open('/tmp/'+key, "r")
        # Load raw data into json
        raw_data = json.load(f)
        order_number = key.replace(".json", "").split("#")[3]

        # Define paramaters for HeaderRecord if
        # order number equal 1
        if(order_number == str(1)):
            version_header = raw_data['header'][0]
            from_participant = raw_data['header'][2]
            to_participant = raw_data['header'][3]
            assumed = bool(raw_data['header'][5])
            if(assumed == "False"):
                assumed = False
            else:
                assumed = True
            # Analyze creation_date
            creation_date = convert_datetime(raw_data['header'][1])
            # Analyze original file name
            file_name = raw_data['header'][4]
            first_hashtag = file_name.find("#")
            second_hashtag = file_name.find("#", first_hashtag+1)
            file_name = file_name[first_hashtag+1:second_hashtag]+".csv"
            # Create header
            header = nem_objects.HeaderRecord(version_header, creation_date,
                                              from_participant, to_participant,
                                              file_name, assumed
                                              )
            readings = {}
            transactions = {}
            # Create readings and transactions
            connect_readings_formatted(readings, raw_data['readings'])
            connect_transaction(transactions, raw_data['transactions'])
            # Put all raw data into container
            raw_data_container['header'] = header
            raw_data_container['readings'] = readings
            raw_data_container['transactions'] = transactions
            os.remove('/tmp/'+key)
            print("Finish remove order number: "+str(order_number))
            f.close()
        # Get all others file
        else:
            # Create readings and transactions
            connect_readings_formatted(readings, raw_data['readings'])
            connect_transaction(transactions, raw_data['transactions'])
            # Put all raw data into container
            raw_data_container['readings'] = readings
            raw_data_container['transactions'] = transactions
            os.remove('/tmp/'+key)
            print("Finish remove order number: "+str(order_number))
            f.close()
    # Define variables for NEMFile
    print("Before open file result")
    f = open('/tmp/raw/Result.txt', 'w')
    print("After open file result")
    for nmi in raw_data_container['readings']:
        for suffix in raw_data_container['readings'][nmi]:
            for reading in raw_data_container['readings'][nmi][suffix]:
                f.write(str(reading)+"\n")
    f.close()
    resource.meta.client.upload_file('/tmp/raw/Result.txt',
                                     bucket_name,
                                     'result/Result.txt')
    print("Fisnist Export Result and Test for sure")
