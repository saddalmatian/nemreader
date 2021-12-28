import boto3
import json

client = boto3.client('lambda')

splitFileEvent = {
    "file_path": "NEM12.csv",
    "line_quantity": 2
}

uploadFileEvent = {
    "Records": [
        {
            "eventVersion": "2.0",
            "eventSource": "aws:s3",
            "awsRegion": "ap-southeast-1",
            "eventTime": "1970-01-01T00:00:00.000Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "EXAMPLE"
            },
            "requestParameters": {
                "sourceIPAddress": "127.0.0.1"
            },
            "responseElements": {
                "x-amz-request-id": "EXAMPLE123456789",
                "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "testConfigRule",
                "bucket": {
                    "name": "nembucket",
                    "ownerIdentity": {
                            "principalId": "EXAMPLE"
                    },
                    "arn": "arn:aws:s3:::example-bucket"
                },
                "object": {
                    "key": "NEM12.csv",
                    "size": 1024,
                    "eTag": "0123456789abcdef0123456789abcdef",
                    "sequencer": "0A1B2C3D4E5F678901"
                }
            }
        }
    ]
}


response = client.invoke(
    FunctionName='splitFileFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps(splitFileEvent),
)


response = client.invoke(
    FunctionName='',
    InvocationType='RequestResponse',
    Payload=json.dumps(splitFileEvent),
)
# return response
print(json.dumps(json.load(response['Payload']), indent=4, sort_keys=True))
