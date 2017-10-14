# -*- coding: utf-8 -*-

from __future__ import absolute_import
import time
import falcon
import logging
from bson import json_util, ObjectId
from uggipuggi import constants
from uggipuggi.controllers.hooks import deserialize, serialize, read_req_body, supply_redis_conn
from uggipuggi.libs.error import HTTPBadRequest
from uggipuggi.messaging.contacts_kafka_producers import contacts_kafka_item_post_producer,\
                                                         contacts_kafka_item_delete_producer


logger = logging.getLogger(__name__)

@falcon.before(supply_redis_conn)
class Item(object):
    def __init__(self):
        self.kafka_topic_name = 'contacts_item'

    @falcon.before(read_req_body)
    @falcon.after(serialize)
    #@falcon.after(contacts_kafka_item_get_producer)
    def on_get(self, req, resp, id):
        # Get all contacts of user
        if id != req.user_id:
            resp.status = falcon.HTTP_UNAUTHORIZED
        else:    
            req.kafka_topic_name = '_'.join([self.kafka_topic_name + req.method.lower()])
            contacts_id_name = 'contacts:' + id
            resp.body = req.redis_conn.smembers(contacts_id_name)
            resp.status = falcon.HTTP_FOUND
        
    @falcon.before(read_req_body)    
    @falcon.after(serialize)
    @falcon.after(contacts_kafka_item_delete_producer)
    def on_delete(self, req, resp, id):
        if id != req.user_id:
            resp.status = falcon.HTTP_UNAUTHORIZED
        else:    
            req.kafka_topic_name = '_'.join([self.kafka_topic_name + req.method.lower()])
            logger.debug("Deleting member from user contacts in database ...")
            contacts_id_name = 'contacts:' + id
            if 'contact_user_id' in req.body:
                req.redis_conn.sdel(contacts_id_name, req.body['contact_user_id'])
                logger.debug("Deleted member from user contacts in database")
                resp.status = falcon.HTTP_OK
            else:
                logger.warn("Please provide contact_user_id to delete from users contact")
                resp.status = falcon.HTTPMissingParam                

    @falcon.before(read_req_body)
    @falcon.after(serialize)
    @falcon.after(contacts_kafka_item_post_producer)
    def on_post(self, req, resp, id):
        if id != req.user_id:
            resp.status = falcon.HTTP_UNAUTHORIZED
        else:
            req.kafka_topic_name = '_'.join([self.kafka_topic_name + req.method.lower()])
            logger.debug("Adding member to user contacts in database ... %s" %repr(id))
            contacts_id_name = 'contacts:' + id
            if 'contact_user_id' in req.body:
                req.redis_conn.sadd(contacts_id_name, req.body['contact_user_id'])
                logger.debug("Added member to user contacts in database")
                resp.status = falcon.HTTP_OK
            else:
                logger.warn("Please provide contact_user_id to add to users contacts")
                resp.status = falcon.HTTPMissingParam
                