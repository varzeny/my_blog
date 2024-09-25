from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category, Tag
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

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

    # 댓글 가져오기
    comments = Comment.objects.filter(post=post, parent=None).order_by('created_at')
    
    context = {
        "post":post,
        "comments":comments,
    }
    return render(req, "app_posting/post.html", context)


@csrf_protect
@require_POST
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # 해당 포스트를 찾습니다.

    # 폼 데이터 받기
    author = request.POST.get('author')
    pw = request.POST.get('pw')
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id', None)  # 대댓글일 경우 부모 댓글 ID

    # 필수 데이터가 누락된 경우 오류 처리
    if not (author and pw and content):
        return HttpResponseBadRequest("Author, password, and content are required.")

    # 부모 댓글이 있는 경우 해당 댓글을 가져옵니다.
    parent_comment = None
    if parent_id:
        parent_comment = get_object_or_404(Comment, id=parent_id)

    # 새로운 댓글 생성
    Comment.objects.create(
        post=post,
        author=author,
        pw=pw,  # 보안을 위해 해시 처리가 필요할 수 있습니다.
        content=content,
        parent=parent_comment
    )

    # 댓글 작성 후 포스트 상세 페이지로 리다이렉트
    return redirect('get_post_by_slug', slug=post.slug)

from django.http import HttpResponse
@csrf_protect
@require_POST
def comment_delete(req):
    id = req.POST.get("comment_id")
    pw = req.POST.get("comment_pw")
    print(id,pw)

    cmt = get_object_or_404(Comment, id=id)

    if cmt.pw == pw:
        cmt.delete()
        return redirect('get_post_by_slug', slug=cmt.post.slug)
    else:
        return HttpResponseBadRequest("wrong pw")
