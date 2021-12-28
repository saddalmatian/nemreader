import boto3

client = boto3.client('lambda')


# Get zip function (handler)
with open('lambda.zip', 'rb') as f:
    zipped_code = f.read()


# Create function
# response = client.create_function(
#     FunctionName='splitNEMFileFunction',
#     Runtime='python3.9',
#     Role='arn:aws:iam::769253686157:role/hoaLambdaBasicRole',
#     Handler='handler.split_file_handler',
#     Code=dict(ZipFile=zipped_code),
#     Timeout=300
# )
# print_json(response)


# Update function
# with open('lambda.zip', 'rb') as f:
#     zipped_code = f.read()
# response = client.update_function_code(
#     FunctionName='helloWorldLambda',
#     ZipFile=zipped_code
# )
