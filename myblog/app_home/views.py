from django.shortcuts import render
from app_posting.models import Post


def get_html_home(req):

    # 조회수가 가장 높은 3개의 포스트를 가져옵니다.
    top_posts = Post.objects.filter(published=True).order_by('-views')[:3]
    
    context = {
        'top_posts': top_posts
    }

    return render(req, "app_home/home.html", context)


def get_html_aboutme(req):
    return render(req, "app_home/aboutme.html")