from .serializers import PostSerializer, UserSerializer
from rest_framework.views import APIView
from .models import PostDetail, User

from rest_framework.response import Response

# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(APIView):
    serializer_class = UserSerializer
    
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
class PostViewSet(APIView):
    serializer_class = PostSerializer
    
    def get(self, request, format=None):
        posts = PostDetail.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, format=None):
        posts = PostDetail.objects.get(id=request.data['id'])
        posts.delete()
        return Response(status=200)
    
    def put(self, request, format=None):
        posts = PostDetail.objects.get(id=request.data['id'])
        posts.post_content = request.data['post_content']
        posts.save()
        return Response(status=200)
    
    
    