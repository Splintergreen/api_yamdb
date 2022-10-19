from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet
)

app_name = 'api'
router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='сategories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [path('v1/', include(router.urls))]
