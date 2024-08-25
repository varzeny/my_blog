from django.urls import path 
from . import views 

 

urlpatterns = [
    path('', views.get_html_posting, name="get_html_posting"),
] 