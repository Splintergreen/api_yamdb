from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, CurrentUser, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

app_name = 'api'
router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='сategories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('auth/signup/', signup, name="signup"),
    path('auth/token/', token, name="token"),
    path('users/me/', CurrentUser.as_view(), name="users/me"),
    path('', include(router.urls)),
]
