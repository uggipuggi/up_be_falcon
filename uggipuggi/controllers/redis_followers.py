# -*- coding: utf-8 -*-

from __future__ import absolute_import
import time
import falcon
import logging
from bson import json_util, ObjectId
from uggipuggi.constants import FOLLOWERS
from uggipuggi.controllers.hooks import deserialize, serialize, supply_redis_conn
from uggipuggi.libs.error import HTTPBadRequest
from uggipuggi.messaging.followers_kafka_producers import followers_kafka_item_delete_producer


logger = logging.getLogger(__name__)

@falcon.before(supply_redis_conn)
@falcon.after(serialize)
class Item(object):
    def __init__(self):
        self.kafka_topic_name = 'followers_item'

    @falcon.before(deserialize)
    #@falcon.after(group_kafka_item_get_producer)
    def on_get(self, req, resp, id):
        # Get all followers of user
        if id != req.user_id:
            resp.status = falcon.HTTP_UNAUTHORIZED
        else:    
            req.kafka_topic_name = '_'.join([self.kafka_topic_name + req.method.lower()])
            followers_id_name = FOLLOWERS + id
            resp.body = req.redis_conn.smembers(followers_id_name)
            resp.status = falcon.HTTP_FOUND
        
    @falcon.before(deserialize)    
    @falcon.after(followers_kafka_item_delete_producer)
    def on_delete(self, req, resp, id):
        if id != req.user_id:
            resp.status = falcon.HTTP_UNAUTHORIZED
        else:    
            req.kafka_topic_name = '_'.join([self.kafka_topic_name + req.method.lower()])
            logger.debug("Deleting member from user followers in database ...")
            followers_id_name = FOLLOWERS + id
            try:
                req.redis_conn.srem(followers_id_name, req.params['query']['follower_user_id'])
                logger.debug("Deleted member from user followers in database")
                resp.status = falcon.HTTP_OK
            except KeyError:
                logger.warn("Please provide contact_user_id to delete from users contact")
                resp.status = falcon.HTTPMissingParam