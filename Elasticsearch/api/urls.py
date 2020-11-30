# from django.urls import path, include
from api import views 
from django.conf.urls import url, include 

urlpatterns = [ 
    url('articles/', views.articles.as_view()),
    url('categories/', views.category.as_view()),
]