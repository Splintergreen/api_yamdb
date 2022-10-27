from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilterSet
from .mixins import ListCreateDestroyMixin
from .permissions import (IsAdminOrReadOnly,
                          IsStaffOrModeratorOrAuthorPermission, StaffOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleAddDataSerializer, TitleGetDataSerializer,
                          TokenSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        email=request.data['email'],
        username=request.data['username'],
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Код подтверждения',
              f'Ваш код подтверждения: {confirmation_code}',
              f"{settings.YAMDB_EMAIL}",
              [request.data['email']],
              fail_silently=False, )
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data["confirmation_code"]
    token = tokens.RefreshToken.for_user(user)
    response_data = {'token': str(token.access_token)}
    if default_token_generator.check_token(user, confirmation_code):
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (StaffOnly,)
    lookup_field = 'username'

    def perform_create(self, serializer):
        if 'role' not in self.request.data:
            serializer.save(role='user')
        serializer.save()

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def current_user_info(self, request):
        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "PATCH":
            serializer.save(role=self.request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg("reviews__score")).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitleAddDataSerializer
        return TitleGetDataSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrModeratorOrAuthorPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrModeratorOrAuthorPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title_id=title_id)
        return Comment.objects.filter(review_id=review.id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title_id=title_id)
        serializer.save(author=self.request.user, review_id=review.id)
