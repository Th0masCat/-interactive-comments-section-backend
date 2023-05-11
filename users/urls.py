from django.urls import path
from .views import PostViewSet, RegisterView, UserViewSet


urlpatterns = [
    path('toka/', PostViewSet.as_view(), name='post'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/', UserViewSet.as_view(), name='user')
]