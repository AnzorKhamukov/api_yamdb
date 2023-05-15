from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet


router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),

]