from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, signup, get_token

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

auth_path = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='get_token')
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(auth_path))
]
