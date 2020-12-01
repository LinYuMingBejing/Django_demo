from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from api.models import Restaurant, Areas, RestaurantTypes
from datetime import datetime


@registry.register_document
class RestaurantDocument(Document):
    
    type = fields.TextField(attr='type_to_string')

    class Index:
        name = 'restaurant'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Restaurant # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'restaurant_id',
            'restaurant',
            'ratings',
            'price',
            'types',
            'areas',
            'spots',
            'created_time',
        ]


    def save(self, ** kwargs):
        self.created_time = datetime.now()
        return super().save(** kwargs)
    

@registry.register_document
class AreasDocument(Document):
    
    type = fields.TextField(attr='type_to_string')

    class Index:
        # Name of the Elasticsearch index
        name = 'restaurant_area'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
        
    class Django:
        model = Areas # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'place',
            'region',
            'location',
            'created_time',
        ]

    
    def save(self, ** kwargs):
        self.created_time = datetime.now()
        return super().save(** kwargs)


@registry.register_document
class RestaurantTypesDocument(Document):
    
    type = fields.TextField(attr='type_to_string')

    class Index:
        # Name of the Elasticsearch index
        name = 'restaurant_category'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}


    class Django:
        model = RestaurantTypes # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'name',
            'subcategory',
            'created_time',
        ]

        
    def save(self, **kwargs):
        self.created_time = datetime.now()
        return super().save(**kwargs)