from django.urls import path 
from . import views 



urlpatterns = [
    path('', views.get_html_posting, name="get_html_posting"),
    path("posts/", views.get_posts_by_slug, name="get_posts_by_slug"),
] 