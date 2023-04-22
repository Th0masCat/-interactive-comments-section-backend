from django.urls import path
from .views import MyTokenObtainPairView, PostViewSet, UserViewSet

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('toka/', PostViewSet.as_view(), name='post'),
    path('user/', UserViewSet.as_view(), name='user')
]