import logging
from confluent_kafka import Producer

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
followers_producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def followers_kafka_item_get_producer(req, resp, resource):
    # This might be useful for number of views for recipe
    parameters = [req.user_id, resp.status]
    logging.debug("++++++++++++++++++++++")
    logging.debug("FOLLOWERS_KAFKA_ITEM_GET_PRODUCER: %s" %req.kafka_topic_name)
    logging.debug("----------------------")
    logging.debug(repr(parameters))
    logging.debug("++++++++++++++++++++++")    
    followers_producer.produce(topic=req.kafka_topic_name, 
                            value=repr(parameters),
                            key=req.params['body']['user_id']) #req.encode('utf-8'))
    followers_producer.flush()
       
def followers_kafka_item_delete_producer(req, resp, resource):
    parameters = [req.user_id, resp.status]
    logging.debug("++++++++++++++++++++++")
    logging.debug("FOLLOWERS_KAFKA_ITEM_DELETE_PRODUCER: %s" %req.kafka_topic_name)
    logging.debug("----------------------")
    logging.debug(repr(parameters))
    logging.debug("++++++++++++++++++++++")
    followers_producer.produce(topic=req.kafka_topic_name, 
                            value=repr(parameters),
                            key=req.params['body']['user_id']) #req.encode('utf-8'))
    followers_producer.flush()
    