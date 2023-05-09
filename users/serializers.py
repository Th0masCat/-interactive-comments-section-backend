from .models import PostDetail, User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['name', 'user_image', 'email']
        

class PostSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='username', read_only=True)
    
    class Meta:
        model = PostDetail
        fields = ['id' , 'username' ,'user_details', 'time_when_posted', 'post_content', 'likes', 'parent_post']
        