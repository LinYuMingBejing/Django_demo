from django.urls import path
from api import views 


urlpatterns = [ 
    path('filter', views.ArticleFilterView.as_view()),
    path('', views.ArticleView.as_view()),

]