from rest_framework_mongoengine import serializers
from api.models import Article

# https://stackoverflow.com/questions/31889076/why-django-rest-framework-mongoengine-serializers-is-valid-always-return-false


class BooksSerializer(serializers.DocumentSerializer):

    class Meta:
        model = Article
        fields = ('title', 'author', 'publisher', 'subCategory', 'price') 