from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=300)

class BlogCreatorPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=300)
    blog_author = models.CharField(max_length=300)
    blog_content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tag = models.CharField(max_length=300)
    publication_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    tag_name = models.CharField(max_length=300)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogcreatorpost = models.ForeignKey(BlogCreatorPost, on_delete=models.CASCADE)
    comment = models.TextField()
    email = models.EmailField(max_length=254)
    publication_date = models.DateTimeField(auto_now_add=True)
    

