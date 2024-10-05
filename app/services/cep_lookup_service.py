import json

import requests
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()


@tracer.capture_method
def lookup_cep(event):
    try:
        body = json.loads(event.get('body', '{}'))
        cep = body.get('cep')
        if not cep:
            raise ValueError("CEP is missing from the request body")

        url = f"https://viacep.com.br/ws/{cep}/json/"
        logger.info(f"Calling external API for CEP {cep}")
        response = requests.get(url=url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
    except requests.RequestException as e:
        logger.error(f"Error calling the external API: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing CEP lookup: {e}")
        raise
    else:
        logger.info(f"API response: {response.json()}")
        return response.json()
