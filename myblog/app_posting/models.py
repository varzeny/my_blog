from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django_comments.models import Comment


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/posting/category/{self.slug}/'
    

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/posting/tag/{self.slug}/'


class Post(models.Model):
    title = models.CharField(max_length=200)  # 포스트의 제목
    slug = models.SlugField(max_length=200, unique=True)  # SEO 친화적인 URL을 위한 슬러그
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relation_post_user')  # 작성자
    excerpt = models.TextField(max_length=500, blank=True, null=True)  # 요약문
    thumbnail = models.ImageField(upload_to='app_posting/thumbnails/%Y/%m/%d/', blank=True, null=True)  # 포스트의 섬네일 이미지
    content = models.TextField()  # 포스트의 본문
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='relation_post_category', null=True)  # 카테고리
    tags = models.ManyToManyField(Tag, blank=True, related_name='relation_post_tag')  # 태그와 다대다 관계
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)  # 수정 날짜
    published_at = models.DateTimeField(default=timezone.now)  # 발행 날짜
    published = models.BooleanField(default=False)  # 발행 여부
    views = models.PositiveIntegerField(default=0)  # 조회수
    comments = GenericRelation(Comment, related_query_name='relation_post_comments')  # 댓글 기능

    class Meta:
        ordering = ['-published_at']  # 기본 정렬 기준: 발행 날짜의 내림차순

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/posting/post/{self.slug}/'
