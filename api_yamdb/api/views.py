from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, User

from .serializers import (CategorySerializer, TitlAddDataSerializer,
                          TitleGetDataSerializer, TokenSerializer,
                          UserSerializer)


@api_view(['POST'])
def signup(request):
    user = request.data
    serializer = UserSerializer(data=user)
    if serializer.is_valid():
        confirmation_code = get_random_string(length=20)
        send_mail('Код подтверждения',
                  f'Ваш код подтверждения: {confirmation_code}',
                  'no-reply@api_yamdb.com',
                  [user['email'], ],
                  fail_silently=False,)
        serializer.save(confirmation_code=confirmation_code)
        return Response(request.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        if User.objects.filter(**request.data).exists():
            user = User.objects.get(**request.data)
            token = RefreshToken.for_user(user)
            response_data = {'token': str(token.access_token)}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(request.data, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = ()

    def perform_create(self, serializer):
        serializer.save()


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = ()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = ()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'

# lookup_expr??
class TitleFilterSet(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')

# rating??
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # permission_classes = ()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitlAddDataSerializer
        return TitleGetDataSerializer
