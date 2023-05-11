from .serializers import PostSerializer
from rest_framework.views import APIView
from .models import PostDetail, User
from django.http import JsonResponse

from rest_framework.response import Response

from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)

class UserViewSet(APIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        if User.objects.filter(name=request.data['name']).exists() and User.objects.get(name=request.data['name']).password == request.data['password']:
            users = User.objects.get(name=request.data['name'])
            serializer = UserSerializer(users, many=False)
            return Response(serializer.data)
        elif User.objects.filter(name=request.data['name']).exists() and User.objects.get(name=request.data['name']).password != request.data['password']:
            return Response(status=400)    

        return Response('User does not exist', status=400)
    
def create_comment_tree(posts):
    tree = {}
    for post in posts:
        tree[post.id] = []
        if post.parent_post:
            tree[post.parent_post.id].append(post.id)
            
    return tree

def buildForest(data, posts):
    nodes = {}
    roots = []

    for key in data.keys():
        value = int(key)
        nodes[value] = {'value': value, 
                'data':{
                'id': posts.get(id=value).id,
                'username': posts.get(id=value).username.name,
                'time_when_posted': posts.get(id=value).time_when_posted,
                'post_content': posts.get(id=value).post_content,
                'likes': posts.get(id=value).likes,
                'parent_post': posts.get(id=value).parent_post.id if posts.get(id=value).parent_post else None,
                'user_details': {
                    'name': posts.get(id=value).username.name,
                    'user_image': posts.get(id=value).username.user_image.url if posts.get(id=value).username.user_image else None,
                    'email': posts.get(id=value).username.email
                }
            }, 'children': []}

    for key, children in data.items():
        node = nodes[int(key)]
        node['children'] = [nodes[child] for child in children]
        node['children'] = sorted(node['children'], key=lambda k: k['data']['time_when_posted'], reverse=True)

        if not any(node['value'] in lst for lst in data.values()):
            roots.append(node)
    
    roots = sorted(roots, key=lambda k: k['data']['time_when_posted'], reverse=True)

    return roots


def refresh_tree():
    posts = PostDetail.objects.all()
    tree = create_comment_tree(posts)
    forest = buildForest(tree, posts)
    
    forest = sorted(forest, key=lambda k: k['data']['time_when_posted'], reverse=True)
    
    return forest

forest = refresh_tree()

class PostViewSet(APIView):
    serializer_class = PostSerializer
    
    def get(self, request, format=None):
        forest = refresh_tree()
        return JsonResponse(forest, safe=False)
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
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
    
    
    