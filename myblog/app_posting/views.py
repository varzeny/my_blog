from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.

def get_html_posting(req):
    # 요구가 있나 확인
    slug = req.GET.get("slug")
    print("@@@@@@@@@@@@@@@@@@",slug)


    # 카테고리와 태그 목록을 가져옵니다.
    context = {
        "categories":Category.objects.all(),
        "tags":Tag.objects.all(),
        "slug":slug
    }

    return render(req, "app_posting/posting.html", context)



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
    
    respData = {
        'posts': posts_data,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
    }
    
    return JsonResponse(respData)


def get_post_by_slug(req, slug):
    post = get_object_or_404(Post, slug=slug, published=True)

    # 조회수 증가
    post.views += 1
    post.save()
    
    context = {
        "post":post,
    }
    return render(req, "app_posting/post.html", context)