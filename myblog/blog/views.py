from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag, Comment
from django.core.paginator import Paginator
from django.db.models import Q


# home ###################################################################
def get_html_home(req):
    return render(req, "blog/home.html")


# profile ###################################################################
def get_html_profile(req):
    return render(req, "blog/profile.html")


# post ###################################################################
def get_html_post(request):
    posts = Post.objects.filter(published=True).order_by('-published_at')
    paginator = Paginator(posts, 10)  # 페이지네이션, 페이지당 10개의 포스트
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/post.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
    })

def post_search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), published=True).order_by('-published_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/post.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'query': query,
    })

def post_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, published=True).order_by('-published_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/post.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'current_category': category,
    })

def post_list_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag, published=True).order_by('-published_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/post.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'current_tag': tag,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'categories': categories,
        'tags': tags,
    })


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        content = request.POST.get('content')

        if name and password and content:
            Comment.objects.create(
                post=post,
                name=name,
                password=password,
                content=content
            )
        return redirect('post_detail', slug=post.slug)

    return redirect('post_detail', slug=post.slug)