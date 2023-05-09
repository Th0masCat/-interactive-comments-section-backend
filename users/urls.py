from django.urls import path
from .views import PostViewSet, UserViewSet


urlpatterns = [
    path('toka/', PostViewSet.as_view(), name='post'),
    path('user/', UserViewSet.as_view(), name='user')
]