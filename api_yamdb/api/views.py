from reviews.models import User, Category, Genre, Title
from .serializers import (CategorySerializer,
                          TitlAddDataSerializer,
                          TitleGetDataSerializer,
                          UserSerializer)
from rest_framework import viewsets, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter, NumberFilter


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
