import json

from aws_lambda_powertools import Logger, Tracer

from repositories import dynamo_repository
from services import cep_service

logger = Logger()
tracer = Tracer()


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    logger.info("Iniciando lambda..")
    try:
        cep_response = cep_service.consulta(event)
        response = dynamo_repository.insert(cep_response)
    except Exception as e:
        print(e)
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
    finally:
        logger.info("Finalizando lambda..")
