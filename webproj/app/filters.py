import django_filters
from django_property_filter import PropertyFilterSet, PropertyNumberFilter, PropertyOrderingFilter
from app.models import Product

class ProductFilter(PropertyFilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', exclude='')
    max_price = PropertyNumberFilter(field_name='price', lookup_expr='lt')
    min_price = PropertyNumberFilter(field_name='price', lookup_expr='gte')
    price = PropertyNumberFilter(field_name='price')
    stars = PropertyNumberFilter(field_name='stars')

    order = PropertyOrderingFilter(
        fields=(
            ('price', 'price'),
            ('stars', 'stars'),
        )
    )


    class Meta:
        model = Product
        fields = ['max_price', 'min_price', 'price', 'stars', 'category', 'developer', 'name']

