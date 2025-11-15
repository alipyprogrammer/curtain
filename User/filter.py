import django_filters
from User.models import User

# class UserFilter(django_filters.FilterSet):
#     class Meta:
#         model = User
#         fields = {
#             'Expert': ['exact'],
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.filters['Expert'] = django_filters.BooleanFilter(
#             field_name='Expert',
#             lookup_expr='exact',
#             label='Is Expert',
#             value=True,
#             method='filter_Expert',
#             widget=django_filters.widgets.BooleanWidget(attrs={'disabled': True})
#         )

#     def filter_Expert(self, queryset, name, value):
#         return queryset.filter(Expert=value)