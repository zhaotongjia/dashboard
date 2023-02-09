import connexion
from connexion import NoContent
import datetime
import json
import logging
import logging.config
import pykafka
from pykafka import KafkaClient
import requests
import uuid
import yaml 

def process_event(event, endpoint):
    trace_id = str(uuid.uuid4())
    event['trace_id'] = trace_id

    logging.debug(f'Received event {endpoint} with trace id: {trace_id}')
    # TODO: call logger.debug and pass in message "Received event <type> with trace id <trace_id>"

    headers = { 'Content-Type': 'application/json' }
    
    url = app_config[endpoint]['url']
    res = requests.post(url, headers=headers, data=json.dumps(event))
    # TODO: update requests.post to use app_config property instead of hard-coded URL
    
    logger.debug(f'Received response with trace id: {trace_id}, status code: {res.status_code}')
    # TODO: call logger.debug and pass in message "Received response with trace id <trace_id>, status code <status_code>"

    # pass
    return res.text, res.status_code

# Endpoints
def buy(body):
    process_event(body, 'buy')
    return NoContent, 201

def sell(body):
    process_event(body, 'sell')
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read()) #use yaml library to read the configuration file

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basic') 
# we mostly deal with the objects of the Logger class, which are instantiated using
# the module-level function loggin.getLogger(name), "name" is a custom logger 
# unlike root logger, it cannot be configured using basicConfig(), have to use Handlers and Formatters

if __name__ == "__main__":
    app.run(port=8080)