import os
import uuid
from datetime import datetime

import boto3
import pytz
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()


@tracer.capture_method
def insert_item(cep_response):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME environment variable is not set")

    table = dynamodb.Table(table_name)
    pk = str(uuid.uuid4())
    saopaulo_tz = pytz.timezone('America/Sao_Paulo')
    sk = datetime.now(saopaulo_tz).isoformat()
    localidade = cep_response.get('localidade')
    if not localidade:
        raise ValueError("Localidade is missing in the CEP response")

    try:
        item = {
                "PK": pk,
                "SK": sk,
                "localidade": localidade
            }
        table.put_item(
            Item=item,
        )
        logger.info("Item successfully inserted")
        return item
    except Exception as e:
        logger.error(f"Error inserting item into DynamoDB: {e}")
        raise
