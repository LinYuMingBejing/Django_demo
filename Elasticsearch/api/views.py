from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.core.cache import cache

from elasticsearch_dsl import Q, query
import elasticsearch_dsl
from datetime import datetime

from api.serializers import RestaurantSerializer
from api.documents import RestaurantDocument, AreasDocument, RestaurantTypesDocument
from AIChoice.settings import REDIS_TIMEOUT


# Create your views here.

class restaurants(APIView):

    def get_area(self, area_ids):
        if not area_ids:
            return
        
        areas = []
        records = AreasDocument.mget(docs= area_ids)
        for record in records:
            if isinstance(record.place, elasticsearch_dsl.utils.AttrList):
                areas.extend(record.place) 
            else:
                areas.append(record.place)
        
        areas = '\"{}\"'.format('" "'.join(list(set(areas))))
        return areas


    def get_subcategory(self, category_ids):
        if not category_ids:
            return
        
        categories = None
        records = RestaurantTypesDocument.mget(docs = category_ids)
        for record in records:
            if not categories:
                categories = '\"{}\"'.format(record.name)
                continue
        
            categories = '{} "{}"'.format(categories, record.name)
                
        return categories


    def get_object(self, areas, categories, updated_date, keywords):
        queryArray = []

        if updated_date:
            end_date = datetime.strptime(updated_date['to'], '%Y-%m-%d')
            start_date = datetime.strptime(updated_date['from'], '%Y-%m-%d')
            queryArray.append(Q('range', created_time = {'gte': start_date, 'lte': end_date}))
            
        if keywords:
            keywords = '\"{}\"'.format('" "'.join(keywords))
            queryArray.append(Q('simple_query_string', fields = ['restaurant'], query = keywords))
        
        if areas:
            queryArray.append(Q('simple_query_string', fields = ['areas'], query = areas))

        if categories:
            queryArray.append(Q('simple_query_string', fields = ['spots', 'types'], query = categories))
        
        query = RestaurantDocument.search().query('bool', must = queryArray)

        restaurants = []
        for restaurant in query.scan():
            row = {}
            row['restaurant'] = restaurant.restaurant
            row['ratings'] = restaurant.ratings
            row['types'] = restaurant.types
            row['areas'] = restaurant.areas
            row['price'] = restaurant.price
            restaurants.append(row)

        return restaurants


    def post(self, request, format=None):
        res  = {'status': False}

        area_ids = request.data.get('areas', None)
        keywords = request.data.get('keywords', None)
        category_ids = request.data.get('subcategory', None)
        updated_date = request.data.get('updated_date', None)

        areas = self.get_area(area_ids)
        categories = self.get_subcategory(category_ids)
        restaurants = self.get_object(areas, categories, updated_date, keywords)
        
        restaurants = RestaurantSerializer(restaurants, many=True).data
        res.update({'status': True, 'data': restaurants})
        return JsonResponse(res, safe=False)


class category(APIView):

    def get_areas(self):
        query = AreasDocument.search().query()
        areas = {}
        for record in query.scan():
            if record.region not in areas:
                areas[record.region] = []
            areas[record.region].append({'id': record.id, 'value': record.location})
        return areas


    def get_categories(self):
        query = RestaurantTypesDocument.search().query()
        categories = {}
        for record in query.scan():
            if record.subcategory not in categories:
                categories[record.subcategory] = []
            categories[record.subcategory].append({'id': record.id, 'value': record.name})
        return categories


    def get(self, format=None):
        res = {'status': False}

        data = cache.get('data')
        if not data:
            data = {}
            data['areas'] = self.get_areas()
            data['categories'] = self.get_categories()
            cache.set('data', data, REDIS_TIMEOUT)
        
        res.update({'status': True, 'data': data})
        return JsonResponse(res)


class upload_restaurant(APIView):

    def post(self, request, format=None):
        res = {'status': False}
        data = request.data.get('data', None)
        restaurant = RestaurantDocument(meta={'id': data['restaurant']}, **data)
        
        # save the document into the cluster
        restaurant.save()
        res.update({'status': True})
        return JsonResponse(res)


class upload_areas(APIView):

    def post(self, request, format=None):
        res = {'status': False}
        data = request.data.get('data', None)
        areas = AreasDocument(meta={'id': data['id']}, **data)
        
        # save the document into the cluster
        areas.save()
        res.update({'status': True})
        return JsonResponse(res)


class upload_category(APIView):

    def post(self, request, format=None):
        res = {'status': False}
        data = request.data.get('data', None)
        types = RestaurantTypesDocument(meta={'id': data['id']}, **data)
        
        # save the document into the cluster
        types.save()
        res.update({'status': True})
        return JsonResponse(res)