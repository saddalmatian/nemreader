import os
from nem12_handler import split_nem12_file
from nem12_handler import PREFIX_FILE
from nem12_handler import get_file_quantity
# lambda response


def split_file_handler(event, context):
    file_path = event['file_path']
    line_quantity = event['line_quantity']
    split_nem12_file(file_path, line_quantity)
    file_quantity = get_file_quantity()
    file_container = []
    for id in range(1, file_quantity+1):
        file_container.append("Created file "+PREFIX_FILE+str(id)+".csv")
    print(file_container)
    return{
        'statusCode': 200,
        'body': event['key1']
    }


# Zip file
os.system('zip lambda.zip handler.py')
