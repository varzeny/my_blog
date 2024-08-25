from django.urls import path 
from . import views 

 

urlpatterns = [
    path('', views.get_html_home, name="get_html_home"),
]