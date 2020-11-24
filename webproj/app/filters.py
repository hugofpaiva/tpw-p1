import django_filters
from django_property_filter import PropertyFilterSet, PropertyNumberFilter, PropertyOrderingFilter
from app.models import Product

class ProductFilter(PropertyFilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', exclude='')
    max_price = PropertyNumberFilter(field_name='price', lookup_expr='lt')
    min_price = PropertyNumberFilter(field_name='price', lookup_expr='gte')
    cost = PropertyNumberFilter(field_name='price')
    rate = PropertyNumberFilter(field_name='stars')

    order = PropertyOrderingFilter(
        fields=(
            ('price', 'cost'),
            ('stars', 'rate'),
        )
    )


    class Meta:
        model = Product
        fields = ['max_price', 'min_price', 'rate', 'category', 'developer', 'name', 'order']

