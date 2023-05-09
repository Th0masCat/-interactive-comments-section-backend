from .serializers import PostSerializer, UserSerializer
from rest_framework.views import APIView
from .models import PostDetail, User
from django.http import JsonResponse

from rest_framework.response import Response

class UserViewSet(APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        if User.objects.filter(name=request.data['name']).exists() and User.objects.get(name=request.data['name']).password == request.data['password']:
            users = User.objects.get(name=request.data['name'])
            serializer = UserSerializer(users, many=False)
            return Response(serializer.data)
        elif User.objects.filter(name=request.data['name']).exists() and User.objects.get(name=request.data['name']).password != request.data['password']:
            return Response(status=401)    
                
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
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
    
    
    