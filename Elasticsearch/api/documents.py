from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from api.models import Restaurant, Areas, RestaurantTypes


@registry.register_document
class RestaurantDocument(Document):
    
    type = fields.TextField(attr='type_to_string')

    class Index:
        name = 'restaurant'

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
        ]


@registry.register_document
class AreasDocument(Document):
    
    type = fields.TextField(attr='type_to_string')

    class Index:
        name = 'restaurant_area'

        
    class Django:
        model = Areas # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'place',
        ]


@registry.register_document
class RestaurantTypesDocument(Document):
    
    type = fields.TextField(attr='type_to_string')

    class Index:
        name = 'restaurant_category'


    class Django:
        model = RestaurantTypes # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'name',
            'subcategory',
        ]