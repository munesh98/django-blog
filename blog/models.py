from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Post(models.Model) :
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,blank=True,related_name="liked_posts")
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    category_type = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images/", default="default.png")
    bio = models.TextField(blank=True, null=True)
