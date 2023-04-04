from django_filters import rest_framework as filters

from reviews.models import Title, User


class TitlesFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genre__slug',
                               lookup_expr='icontains')
    name = filters.CharFilter(field_name='name',
                              lookup_expr='icontains')

    class Meta:
        model = Title
        fields = '__all__'


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(
        field_name='username', lookup_expr='exact'
    )

    class Meta:
        model = User
        fields = ('username',)
