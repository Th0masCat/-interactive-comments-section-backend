from .models import PostDetail, User
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['name', 'user_image', 'email', 'password']
        extra_kwargs = {
            'name': {'required': True},
            'password': {'required': True}
        }


    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            user_image=validated_data['user_image'],
            password=validated_data['password']
        )

        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['name', 'user_image', 'email']
        

class PostSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='username', read_only=True)
    
    class Meta:
        model = PostDetail
        fields = ['id' , 'username' ,'user_details', 'time_when_posted', 'post_content', 'likes', 'parent_post']
        