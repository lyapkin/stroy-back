import os
import math
from time import time
from django.utils.text import slugify
from unidecode import unidecode
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from urllib.parse import urljoin
from datetime import datetime
from time import time


def slugify_filename(filename):
    filename_split = filename.split(".")
    no_extention_filename = "_".join(filename_split[:-1]).strip("-_")
    extention = filename_split[-1]
    return f"{slugify(unidecode(no_extention_filename))}-{int(time() * 1000)}.{extention}"


def category_group_image_upload_to(instance, filename):
    new_filename = slugify_filename(filename)
    return "images/catalog/category_group/{slug}/{filename}".format(filename=new_filename, slug=instance.slug)


def product_image_upload_to(instance, filename):
    new_filename = slugify_filename(filename)
    return "images/catalog/product/{slug}/{filename}".format(filename=new_filename, slug=instance.product.slug)


def product_file_upload_to(instance, filename):
    new_filename = slugify_filename(filename)
    return "docs/catalog/product/{slug}/{filename}".format(filename=new_filename, slug=instance.product.slug)


def post_preview_upload_to(instance, filename):
    new_filename = slugify_filename(filename)
    return "images/blog/post/{slug}/{filename}".format(filename=new_filename, slug=instance.slug)


def generate_unique_slug(klass, field):
    origin_slug = slugify(unidecode(field))
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{origin_slug}-{numb}"
        numb += 1
    return unique_slug


class CustomStorage(FileSystemStorage):
    """
    Кастомное расположение для медиа файлов редактора
    """

    def get_folder_name(self, path):
        return os.path.join(*path)

    def get_valid_name(self, name):
        return slugify_filename(name)

    def save(self, name, content, max_length=None):
        folder_name = self.get_folder_name(content.path)
        name = os.path.join(folder_name, self.get_valid_name(name))
        return super().save(name, content, max_length)

    location = os.path.join(settings.MEDIA_ROOT, "ckeditor")
    base_url = urljoin(settings.MEDIA_URL, "ckeditor/")


def is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


def calculate_item_price(price, discount):
    return price if not discount else math.ceil(price * ((100 - discount) / 100))


def calculate_price(quantities: dict[str, str], products: dict[int]) -> dict[int, int]:
    result = {}
    for key in quantities:
        count = int(quantities[key])
        price = products[int(key)].price
        discount = products[int(key)].discount
        result_price = calculate_item_price(price, discount)
        result[int(key)] = result_price * count

    return result


def category_group_image_upload_to(instance, filename):
    new_filename = slugify_filename(filename)
    return "images/catalog/category_group/{slug}/{filename}".format(filename=new_filename, slug=instance.slug)


def product_image_upload_to(instance, filename):
    new_filename = slugify_filename(filename)
    return "images/catalog/product/{slug}/{filename}".format(filename=new_filename, slug=instance.product.slug)


def product_file_upload_to(instance, filename):
    new_filename = slugify_filename(filename)
    return "docs/catalog/product/{slug}/{filename}".format(filename=new_filename, slug=instance.product.slug)


def commercial_request_file_upload_to(instance, filename):
    new_filename = slugify_filename(filename)
    return "docs/requests/commercial/{filename}".format(filename=new_filename)
