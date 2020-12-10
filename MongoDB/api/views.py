from api.models import Article
from api.serializers import BooksSerializer

from rest_framework_mongoengine import generics
from django.http import JsonResponse


# Create your views here.
class ArticleView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = BooksSerializer


class ArticleFilterView(generics.GenericAPIView):
    serializer_class = BooksSerializer
    filter_fields = ('title', 'publisher', 'author')


    def get_kwargs_for_filtering(self):
        filtering_kwargs = {} 

        for field in self.filter_fields: # iterate over the filter fields
            field_value = self.request.query_params.get(field) # get the value of a field from request query parameter
            if field_value: 
                filtering_kwargs[field] = field_value
        return filtering_kwargs 
    

    def get_queryset(self):
        filtering_kwargs = self.get_kwargs_for_filtering()
        if filtering_kwargs:
            queryset = Article.objects.filter(**filtering_kwargs)
        return queryset
    

    def get(self, request, *args, **krgs):
        res = {'status': True}
        books = self.get_queryset()
        serializer = self.serializer_class(books, many=True)
        res['data'] = serializer.data
        return JsonResponse(res, safe=False)
