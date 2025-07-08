from django_filters import rest_framework as filters
from django.db.models import F, Q, Case, When, OuterRef, Subquery
from rest_framework import filters as drf_filters
from .models import Product, ProductPrice


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name="category__slug",
        lookup_expr="iexact",
    )
    group = filters.CharFilter(
        field_name="category__group__slug",
        lookup_expr="iexact",
    )

    class Meta:
        model = Product
        fields = (
            "category",
            "stock",
            "group",
        )

    def fitler_attributes(self, qs):
        attributes = self.request.query_params.getlist("attributes", [])
        if attributes:
            attrs = {}
            for attr in attributes:
                key, value = attr.split(":")
                if key in attrs:
                    attrs[key] |= Q(attributes__attribute__name=key, attributes__value__name=value)
                else:
                    attrs[key] = Q(attributes__attribute__name=key, attributes__value__name=value)
            for key in attrs:
                qs = qs.filter(attrs[key])
            return qs
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

                # return queryset.annotate(
                #     result_price=Case(
                #         When(discount=None, then="price"), default=F("price") - F("price") * F("discount") / 100
                #     )
                # ).order_by(*new_ordering)
                return queryset.annotate(
                    result_price=Subquery(
                        ProductPrice.objects.filter(product=OuterRef("pk"))
                        .annotate(
                            result_price=Case(
                                When(discount=None, then="price"),
                                default=F("price") - F("price") * F("discount") / 100,
                            )
                        )
                        .order_by(*new_ordering)
                        .values("result_price")[:1]
                    )
                ).order_by(*new_ordering)
            return queryset.order_by(*new_ordering)

        return queryset


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class CartFilter(filters.FilterSet):
    id = NumberInFilter(field_name="prices__id", lookup_expr="in")

    class Meta:
        model = Product
        fields = ["id"]
