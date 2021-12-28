import os
from nem12_handler import split_nem12_file
from nem12_handler import PREFIX_FILE
from nem12_handler import get_file_quantity
# lambda response


def split_file_handler(event, context):
    # define paramaters
    file_path = event['file_path']
    line_quantity = event['line_quantity']
    # split file
    split_nem12_file(file_path, line_quantity)
    file_quantity = get_file_quantity()
    file_container = []
    # get files splitted
    for id in range(1, file_quantity+1):
        file_container.append("Created file "+PREFIX_FILE+str(id)+".csv")

    return{
        'statusCode': 200,
        'body': {
            'file_created': file_container
        }
    }


# Zip file
os.system('zip split_file_lambda.zip split_file_handler.py')
