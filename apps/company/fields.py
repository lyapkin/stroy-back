import re
from django.db import models
from django.core.validators import RegexValidator
from django.forms import fields
from django.core.exceptions import ValidationError
from .utils import mask_number


# class PhoneFormField(fields.CharField):

#     def __init__(
#         self,
#         max_length=...,
#         min_length=...,
#         strip=...,
#         empty_value=...,
#         required=...,
#         widget=...,
#         label=...,
#         initial=...,
#         help_text=...,
#         error_messages=...,
#         show_hidden_initial=...,
#         validators=...,
#         localize=...,
#         disabled=...,
#         label_suffix=...,
#     ):
#         initial = mask_number(initial)
#         super().__init__(
#             max_length,
#             min_length,
#             strip,
#             empty_value,
#             required,
#             widget,
#             label,
#             initial,
#             help_text,
#             error_messages,
#             show_hidden_initial,
#             validators,
#             localize,
#             disabled,
#             label_suffix,
#         )

#     def clean(self, value):
#         result = re.match(r"^\+\d{9,19}$", value) or re.match(r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$", value)
#         if result is None:
#             raise ValidationError("Номер телефона указан неверно")
#         value = super().clean(value)

#         return value


class PhoneField(models.CharField):
    default_validators = [RegexValidator(r"^\+\d{9,19}$", "Номер телефона указан неверно")]

    def clean(self, value, model_instance):
        return super().clean(value, model_instance)

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 20
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        return super().formfield(**kwargs)

    def to_python(self, value):
        result = super().to_python(value)
        return "+" + "".join(c for c in result if c.isdigit())

    def pre_save(self, model_instance, add):
        result = super().pre_save(model_instance, add)
        return "+" + "".join(c for c in result if c.isdigit())
