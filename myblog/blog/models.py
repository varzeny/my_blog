from django.db import models

# Create your models here.


# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
#     content = models.TextField()
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
#     published = models.BooleanField(default=False)


#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return f'/blog/{self.slug}/'