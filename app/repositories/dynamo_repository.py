import os

import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()


@tracer.capture_method
def insert(cep_response):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    table = dynamodb.Table(table_name)
    localidade = cep_response.get('localidade')

    response = table.put_item(
        Item={
            "localidade": localidade
        }
    )
    logger.info(f'Item inserido: {response}')
    return response
