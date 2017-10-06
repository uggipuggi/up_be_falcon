# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo
from uggipuggi.constants import TWEET_CHAR_LENGTH

class Recipe(mongo.DynamicDocument):
    recipe_name        = mongo.StringField(required=True)
    user_id            = mongo.StringField(required=True)
    steps              = mongo.ListField(required=True)
    ingredients        = mongo.ListField(required=True) #Ingredients names
    ingredients_ids    = mongo.ListField(required=True) #Ingredients ids
    ingredients_quant  = mongo.ListField(required=True) 
    ingredients_metric = mongo.ListField(required=True)
    ingredients_imgs   = mongo.ListField(mongo.URLField()) # list of urls of ingredients images
    likes_count        = mongo.IntField(required=True, default=0)
    tips               = mongo.ListField(required=False)    
    description        = mongo.StringField(max_length=TWEET_CHAR_LENGTH)
    images             = mongo.ListField(mongo.URLField())  # list of urls
    tags               = mongo.ListField()
    category           = mongo.ListField()         # Should this be a class?
    rating_count       = mongo.IntField(default=0)
    shares_count       = mongo.IntField(default=0)
    rating_total       = mongo.FloatField(default=0)
    prep_time          = mongo.IntField(default=0) # In minutes   
    cook_time          = mongo.IntField(default=0) # In minutes   
    last_modified      = mongo.DateTimeField()
    
    @property
    def rating(self):
        if self.rating_count < 1:
            return 0.00
        return float(self.rating_total / float(self.rating_count))
        
    @property
    def creation_stamp(self):
        # Time created can be obtained from the object _id attribute
        # sort by field _id and you'll get documents in creation time order
        return self.id.generation_time        
    
class Comment(mongo.DynamicDocument):
    user_id      = mongo.StringField(required=True)
    recipe_id    = mongo.StringField(required=True)
    description  = mongo.StringField(max_length=TWEET_CHAR_LENGTH)
    time_stamp   = mongo.DateTimeField()
    
    @property
    def creation_stamp(self):
        # Time created can be obtained from the object _id attribute
        # sort by field _id and you'll get documents in creation time order
        return self.id.generation_time
    
#class Ingredients(mongo.DynamicDocument):
    #recipe = mongo.ReferenceField(Recipe, dbref=True, reverse_delete_rule=mongo.CASCADE)
    #ingredients = mongo.ListField(required=True)
    
#class RecipeSteps(mongo.DynamicDocument):
    #recipe = mongo.ReferenceField(Recipe, dbref=True, reverse_delete_rule=mongo.CASCADE)
    #recipesteps = mongo.ListField(required=True)
    