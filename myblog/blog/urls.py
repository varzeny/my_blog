from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_html_home, name="get_html_home"),
    path("profile", views.get_html_profile, name="get_html_profile"),
    path("post",views.get_html_post, name="get_html_post"),

    path('search/', views.post_search, name='post_search'),  # 검색 결과
    path('category/<slug:category_slug>/', views.post_list_by_category, name='post_list_by_category'),  # 카테고리별 포스트
    path('tag/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),  # 태그별 포스트
    path('<slug:slug>/', views.post_detail, name='post_detail'),  # 개별 포스트 상세 페이지
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),  # 댓글 추가 URL 패턴
]