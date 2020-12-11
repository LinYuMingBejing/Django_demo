from api.models import Article
from api.serializers import BooksSerializer

from rest_framework_mongoengine import generics
from django.http import JsonResponse


# Create your views here.
class ArticleView(generics.ListCreateAPIView):
    queryset = Article.objects.limit(100)
    serializer_class = BooksSerializer


class ArticleFilterView(generics.GenericAPIView):
    serializer_class = BooksSerializer
    filter_fields = ('title', 'publisher', 'author', 'subCategory', 'price__lte', 'price__gte')


    def get_kwargs_for_filtering(self):
        filtering_kwargs = {} 

        for field in self.filter_fields:
            field_value = self.request.query_params.get(field)
            if not field_value: continue
            if 'price' in field_value: 
                filtering_kwargs[field] = int(field_value)
            filtering_kwargs[field] = field_value
        return filtering_kwargs 
    

    def get_queryset(self):
        filtering_kwargs = self.get_kwargs_for_filtering()
        if filtering_kwargs:
            queryset = Article.objects.filter(**filtering_kwargs)\
                                        .order_by('published_date')\
                                        .limit(100)
        return queryset
    

    def get(self, request, *args, **krgs):
        res = {'status': False}
        try:
            books = self.get_queryset()
            serializer = self.serializer_class(books, many=True)
            res.update({'status': True, 'data': serializer.data})
            return JsonResponse(res, safe=False)

        except Exception as e:
            res['msg'] = e
            return JsonResponse(res, safe=False)
