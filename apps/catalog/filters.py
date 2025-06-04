from django_filters import rest_framework as filters
from django.db.models import F, Q, Case, When, Value
from rest_framework import filters as drf_filters
from .models import Product, ProductCategoryGroup, ProductCategory, ProductAttribute


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name="category__slug",
        lookup_expr="iexact",
        # to_field_name="slug",
        # queryset=ProductCategory.objects.all(),
    )
    # id = filters.AllValuesMultipleFilter(field_name="id")
    group = filters.CharFilter(
        field_name="category__group__slug",
        # to_field_name="slug",
        # queryset=ProductCategoryGroup.objects.all(),
        lookup_expr="iexact",
    )

    class Meta:
        model = Product
        fields = (
            "category",
            "stock",
            # "id",
            "group",
        )

    def fitler_attributes(self, qs):
        attributes = self.request.query_params.getlist("attributes", [])
        if attributes:
            q_objects = Q()
            for attr in attributes:
                key, value = attr.split(":")
                q_objects |= Q(attributes__attribute__name=key, attributes__value__name=value)
            return qs.filter(q_objects)
        return qs

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        return self.fitler_attributes(qs)


class PriceOrderingFilter(drf_filters.OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            new_ordering = []
            price = False
            for field in ordering:
                if field == "price":
                    price = True
                    new_ordering.append("result_price")
                elif field == "-price":
                    price = True
                    new_ordering.append("-result_price")
                else:
                    new_ordering.append(field)
            if price:

                return queryset.annotate(
                    result_price=Case(
                        When(discount=None, then="price"), default=F("price") - F("price") * F("discount") / 100
                    )
                ).order_by(*new_ordering)
            return queryset.order_by(*new_ordering)

        return queryset


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class CartFilter(filters.FilterSet):
    id = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = Product
        fields = ["id"]
