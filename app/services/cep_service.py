import json

import requests
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()


@tracer.capture_method
def consulta(event):
    try:
        body = json.loads(event['body'])
        cep = body['cep']
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url=url)
    except Exception as e:
        logger.error(f"Erro na chamada da API: {e}")
    else:
        return response.json()
