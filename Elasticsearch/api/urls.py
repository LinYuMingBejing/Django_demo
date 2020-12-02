# from django.urls import path, include
from api import views 
from django.conf.urls import url, include 

urlpatterns = [ 
    url('articles/', views.restaurants.as_view()),
    url('categories/', views.category.as_view()),
    url('recommend/', views.recommend.as_view()),
    url('update/restaurant/', views.upload_restaurant.as_view()),
    url('update/areas/', views.upload_areas.as_view()),
    url('update/category/', views.upload_category.as_view()),
]