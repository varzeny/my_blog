from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.

def get_html_posting(req):
    
    # 카테고리와 태그 목록을 가져옵니다.
    respData = {
        "categories":Category.objects.all(),
        "tags":Tag.objects.all()
    }

    return render(req, "app_posting/posting.html", respData)



def get_posts_by_slug(req):
    slug = req.GET.get("slug")
    page_number = req.GET.get("page", 1)
    
    # 카테고리나 태그에 해당하는 포스트를 가져옵니다.
    category = Category.objects.filter(slug=slug).first()
    tag = Tag.objects.filter(slug=slug).first()

    if category:
        post_list = Post.objects.filter(category=category, published=True)
    elif tag:
        post_list = Post.objects.filter(tags=tag, published=True)
    else:
        return JsonResponse({'error': 'Invalid category or tag'}, status=400)
    
    paginator = Paginator(post_list, 3)  # 페이지당 n개의 포스트를 표시
    page_obj = paginator.get_page(page_number)
    
    posts_data = [
        {
            'title': post.title,
            'excerpt': post.excerpt,
            'slug': post.slug,
            'thumbnail': post.thumbnail.url if post.thumbnail else '',
        }
        for post in page_obj
    ]
    
    data = {
        'posts': posts_data,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
    }
    
    return JsonResponse(data)