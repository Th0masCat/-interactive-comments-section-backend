from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32, primary_key=True, unique=True)
    email = models.EmailField(max_length=32, unique=True)
    user_image = models.ImageField(upload_to='user_images', blank=True, null=True)
    password = models.CharField(max_length=32, default="password")
    
    def __str__(self):
        return self.name
    

class PostDetail(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    time_when_posted = models.DateTimeField(auto_now_add=True) 
    post_content = models.TextField()
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.post_content
