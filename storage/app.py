import datetime
import json

import connexion
from connexion import NoContent
import swagger_ui_bundle

import mysql.connector 
import pymysql
import yaml
import logging
import logging.config

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from buy import Buy
from sell import Sell

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

# TODO: create connection string, replacing placeholders below with variables defined in log_conf.yml
user = app_config['user']
password = app_config['password']
hostname = app_config['hostname']
port = app_config['port']
db = app_config['db']
DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

# Endpoints
def buy(body):
    # TODO create a session
    session=DB_SESSION()

    # TODO additionally pass trace_id (along with properties from Lab 2) into Buy constructor
    buyobject = Buy(
        body['buy_id'],
        body['item_name'],
        body['item_price'],
        body['buy_qty'],
        body['trace_id']
        # no need to pass date_created, it will be generated everytime Buy class is called in the Class function.
    )
    # TODO add, commit, and close the session
    session.add(buyobject)
    session.commit()
    # session.close()
    # TODO: call logger.debug and pass in message "Stored buy event with trace id <trace_id>"
    logger.debug(f'Stored buy event with trace id {buyobject.trace_id}')
    # TODO return NoContent, 201
    return NoContent, 201
# end

def get_buys(timestamp):
    # create a session 

    data = []
    session=DB_SESSION()
    rows = session.query(Buy).filter(Buy.date_created >= timestamp)
    # rows = session.query(f"SELECT * FROM table WHERE UNIX_TIMESTAMP(data_created) >= {timestamp} ORDER BY data_created DESC LIMIT 10").all()
    # query for all the events since this timestamp
    # rows = session.query.(sell).filter(see.data_created >= timestamp)
    
    # loop through rows, for each row call .to_dic(), then append the dict to data
    for row in rows:
        data.append(row.to_dict())


    print(data)

    return data, 200

def sell(body):
    # TODO create a session
    session=DB_SESSION()
    # TODO additionally pass trace_id (along with properties from Lab 2) into Sell constructor
    sellobject = Sell(
        body['sell_id'],
        body['item_name'],
        body['item_price'],
        body['sell_qty'],
        body['trace_id']
    )
    # TODO add, commit, and close the session
    session.add(sellobject)
    session.commit()
    # session.close()

    # TODO: call logger.debug and pass in message "Stored sell event with trace id <trace_id>"
    logger.debug(f'Stored sell event with trace id {sellobject.trace_id}')

    return NoContent, 201
# end

def get_sells(timestamp):
    data = []
    session=DB_SESSION()
    rows = session.query(Sell).filter(Sell.date_created >= timestamp)
    for row in rows:
        data.append(row.to_dict())


    print(data)
    return data, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api('openapi.yaml', strict_validation=True, validate_responses=True)

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basic')

if __name__ == "__main__":
    app.run(port=8090)