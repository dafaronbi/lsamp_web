import django_filters
from .models import user

class name_filter(django_filters.FilterSet):
    class Meta:
        model = user
        fields = ['lName']