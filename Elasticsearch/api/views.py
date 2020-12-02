from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.core.cache import cache

import elasticsearch_dsl
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import MoreLikeThis
from datetime import datetime

from api.serializers import RestaurantSerializer
from api.documents import RestaurantDocument, AreasDocument, RestaurantTypesDocument
from AIChoice.settings import REDIS_TIMEOUT


# Create your views here.

class restaurants(APIView):

    def get_area(self, area_ids):
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
        categories = None
        records = RestaurantTypesDocument.mget(docs = category_ids)
        for record in records:
            if not categories:
                categories = '\"{}\"'.format(record.name)
                continue
            categories = '{} "{}"'.format(categories, record.name)
                
        return categories


    def get_object(self, area_ids, category_ids, updated_date, keywords):
        queryArray = []

        if updated_date:
            end_date = datetime.strptime(updated_date['to'], '%Y-%m-%d')
            start_date = datetime.strptime(updated_date['from'], '%Y-%m-%d')
            queryArray.append(Q('range', created_time = {'gte': start_date, 'lte': end_date}))
            
        if keywords:
            keywords = '\"{}\"'.format('" "'.join(keywords))
            queryArray.append(Q('simple_query_string', fields = ['restaurant'], query = keywords))
        
        if area_ids:
            areas = self.get_area(area_ids)
            queryArray.append(Q('simple_query_string', fields = ['areas'], query = areas))

        if category_ids:
            categories = self.get_subcategory(category_ids)
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
        """根據條件查詢相關餐廳功能"""
        res  = {'status': False}

        area_ids = request.data.get('areas', None)
        keywords = request.data.get('keywords', None)
        category_ids = request.data.get('subcategory', None)
        updated_date = request.data.get('updated_date', None)

        restaurants = self.get_object(area_ids, category_ids, updated_date, keywords)
        
        restaurants = RestaurantSerializer(restaurants, many=True).data
        res.update({'status': True, 'data': restaurants})
        return JsonResponse(res, safe=False)


class recommend(APIView):

    def get(self, request, format=None):
        """推薦相似餐廳功能"""
        res  = {'status': False}

        restaurant = request.GET.get('restaurant', '')

        text = {'_index':'restaurant', '_type' : '_doc', '_id' : restaurant}

        query = RestaurantDocument.search()\
                                .query(MoreLikeThis(like = text, fields = ['descriptions'], min_term_freq = 1, max_query_terms = 5))\
                                .source(excludes=['descriptions', 'created_time'])

        pages = []
        for restaurant in query.execute():
            pages.append({'title': restaurant.restaurant})
        res.update({'status': True, 'data': pages})

        return JsonResponse(res)


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
        """查詢地區及分類清單的功能"""
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
        """餐廳資訊存儲功能"""
        res = {'status': False}
        data = request.data.get('data', None)

        if 'restaurant' not in data or 'ratings' not in data or 'price' not in data or \
            'types' not in data or 'areas' not in data or 'spots' not in data or 'descriptions' not in data:
            res['msg'] = 'Lack of required parameters'
            return JsonResponse(res)

        RestaurantDocument(meta={'id': data['restaurant']}, **data).save()
        
        res.update({'status': True})
        return JsonResponse(res)


class upload_areas(APIView):

    def post(self, request, format=None):
        """地區資訊存儲功能"""
        res = {'status': False}
        data = request.data.get('data', None)

        if 'location' not in data or 'place' not in data or 'region' not in data:
            res['msg'] = 'Lack of required parameters'
            return JsonResponse(res)
        AreasDocument(meta={'id': data['id']}, **data).save()
        
        res.update({'status': True})
        return JsonResponse(res)


class upload_category(APIView):

    def post(self, request, format=None):
        """分類資訊存儲功能"""
        res = {'status': False}
        data = request.data.get('data', None)

        if 'id' not in data or 'name' not in data or 'subcategory' not in data:
            res['msg'] = 'Lack of required parameters'
            return JsonResponse(res)

        RestaurantTypesDocument(meta={'id': data['id']}, **data).save()
        
        res.update({'status': True})
        return JsonResponse(res)