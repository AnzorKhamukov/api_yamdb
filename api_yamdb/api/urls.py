from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, signup, get_token, CommentViewSet
from .views import TitleViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet


v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'users', UserViewSet, basename='users')


auth_path = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='get_token')
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(auth_path))
]
