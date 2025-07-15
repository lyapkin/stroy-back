from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring
from django.db.models import Prefetch, F, Case, When
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import mixins, viewsets, filters
from django_filters import rest_framework as django_filters
from shared.paginations import BasePagination
from shared.utils import is_int
from .models import (
    ProductCategory,
    ProductCategoryGroup,
    Product,
    ProductAttribute,
    Attribute,
    ProductPrice,
    ProductRedirectFrom,
    ProductCategoryRedirectFrom,
    ProductCategoryGroupRedirectFrom,
)
from .serializers import (
    ProductCategoryGroupSerializer,
    ProductCategoryItemSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCartSerializer,
    ProductRemainderSerializer,
    AttributeSerializer,
)
from .filters import ProductFilter, CartFilter, PriceOrderingFilter


# Create your views here.
class ProductCategoryGroupApi(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategoryGroup.objects.prefetch_related("categories").all()
    serializer_class = ProductCategoryGroupSerializer
    lookup_field = "slug"

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            return super().retrieve(request, slug, *args, **kwargs)
        except Http404:
            active_slug = get_object_or_404(ProductCategoryGroupRedirectFrom, old_slug=slug)
            return redirect(f"/{active_slug.to.slug}/", permanent=True)


class ProductCategoryApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = ProductCategory.objects.select_related("group").all()
    serializer_class = ProductCategoryItemSerializer
    lookup_field = "slug"

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            return super().retrieve(request, slug, *args, **kwargs)
        except Http404:
            active_slug = get_object_or_404(ProductCategoryRedirectFrom, old_slug=slug)
            return redirect(f"/{active_slug.to.group.slug}/{active_slug.to.slug}/", permanent=True)


# product
class ProductApi(viewsets.ReadOnlyModelViewSet):
    queryset_by_action = {
        "list": Product.objects.select_related("category").prefetch_related(
            "images",
            Prefetch(
                "prices",
                queryset=ProductPrice.objects.annotate(
                    result_price=Case(
                        When(discount=None, then="price"), default=F("price") - F("price") * F("discount") / 100
                    )
                ).order_by("result_price"),
            ),
            Prefetch(
                "attributes",
                queryset=ProductAttribute.objects.select_related("attribute", "value"),
            ),
        ),
        "retrieve": Product.objects.prefetch_related(
            "prices",
            "images",
            "docs",
            Prefetch(
                "attributes",
                queryset=ProductAttribute.objects.select_related("attribute", "value"),
            ),
        ),
        "remainder": Product.objects.prefetch_related("images").filter(remainder__isnull=False),
    }
    serializer_action_classes = {
        "list": ProductListSerializer,
        "retrieve": ProductDetailSerializer,
        "remainder": ProductRemainderSerializer,
    }
    lookup_field = "slug"
    pagination_class = BasePagination
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, PriceOrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name"]
    ordering_fields = ["price"]

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def get_queryset(self):
        qs = self.queryset_by_action[self.action]
        return qs.all().distinct()

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            return super().retrieve(request, slug, *args, **kwargs)
        except Http404:
            active_slug = get_object_or_404(ProductRedirectFrom, old_slug=slug)
            return redirect(f"/{active_slug.to.slug}/", permanent=True)

    @action(detail=False)
    def remainder(self, request):
        qs = self.get_queryset().filter(remainder__gt=0)
        serializer = self.get_serializer_class()
        serializer = serializer(qs, context={"request": request}, many=True)
        return Response(serializer.data, status=200)


# cart
class CartApi(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ProductCartSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = CartFilter

    def get_queryset(self):
        ids = self.request.query_params.get("id").split(",")
        ids = [i for i in ids if is_int(i)]
        return Product.objects.prefetch_related(
            "images",
            Prefetch(
                "attributes",
                queryset=ProductAttribute.objects.select_related("attribute", "value"),
            ),
            Prefetch(
                "prices",
                queryset=ProductPrice.objects.filter(id__in=ids),
            ),
        ).distinct()

    @action(detail=False, methods=["get"])
    def exist(self, request):
        ids = request.query_params.get("id", "")
        if bool(ids):
            ids = ids.split(",")
            ids = [i for i in ids if is_int(i)]
            return Response(ProductPrice.objects.filter(id__in=ids).values_list("id", flat=True))

        return Response([])


# attributes
class AttributeApi(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Attribute.objects.prefetch_related("values")
    serializer_class = AttributeSerializer

    def get_queryset(self):
        if self.kwargs.get("category_slug"):
            return self.queryset.filter(category__slug=self.kwargs.get("category_slug"))
        return super().get_queryset()


# for admin script
@api_view(["GET"])
def category_attributes(request, id):
    attrs = ProductCategory.objects.get(id=id).attributes.all().values_list("id", "name")
    return Response(attrs)


@api_view(["GET"])
def attribute_values(request, id):
    attrs = Attribute.objects.get(id=id).values.all().values_list("id", "name")
    return Response(attrs)


# yandex feed
@api_view(["GET"])
def ya_feed(request):
    root = Element("yml_catalog", attrib={"date": str(datetime.now().astimezone().isoformat())})
    shop = SubElement(root, "shop")

    name = SubElement(shop, "name")
    name.text = "Строительные технологии"

    company = SubElement(shop, "company")
    company.text = 'ООО "Строитльные технологии"'

    url = SubElement(shop, "url")
    url.text = settings.SITE_DOMAIN

    currencies = SubElement(shop, "currencies")
    currency = SubElement(currencies, "currency", attrib={"id": "RUB", "rate": "1"})

    categories = SubElement(shop, "categories")
    for cat in ProductCategoryGroup.objects.all():
        category = SubElement(categories, "category", attrib={"id": str(cat.id)})
        category.text = cat.name

    offers = SubElement(shop, "offers")
    products = (
        ProductPrice.objects.prefetch_related("product")
        .annotate(
            result_price=Case(
                When(discount=None, then="price"),
                default=F("price") - F("price") * F("discount") / 100,
            )
        )
        .all()
    )
    for product in products:
        offer = SubElement(offers, "offer", attrib={"id": str(product.id)})
        name = SubElement(offer, "name")
        name.text = f"{product.product.name}{" " + product.name if product.name else ""}"
        url = SubElement(offer, "url")
        url.text = f"{settings.SITE_DOMAIN}/product/{product.product.slug}/"
        price = SubElement(offer, "price")
        price.text = str(product.result_price)
        if product.discount:
            oldPrice = SubElement(offer, "oldprice")
            oldPrice.text = str(product.price)
        currencyId = SubElement(offer, "currencyId")
        currencyId.text = "RUB"
        categoryId = SubElement(offer, "categoryId")
        categoryId.text = str(product.product.category.group.id)
        picture = SubElement(offer, "picture")
        picture.text = settings.SITE_DOMAIN + product.product.first_image.url if product.product.first_image else ""
        description = SubElement(offer, "description")
        description.text = f"<![CDATA[{product.product.description}]]>"

    xml_string = tostring(root, encoding="utf-8", xml_declaration=True)
    return HttpResponse(xml_string, content_type="application/xml")
