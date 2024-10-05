import json

from aws_lambda_powertools import Logger, Tracer
from repositories.dynamodb_repository import insert_item
from services.cep_lookup_service import lookup_cep

logger = Logger()
tracer = Tracer()


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    logger.info("Starting lambda execution...")
    
    try:
        cep_response = lookup_cep(event)
        response = insert_item(cep_response)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
    finally:
        logger.info("Lambda execution finished.")
