from django.db import models
from .fields import PhoneField


# Create your models here.
class Contact(models.Model):
    email = models.EmailField("основной email")
    phone = PhoneField("основной номер телефона")

    class Meta:
        verbose_name = "контакты"
        verbose_name_plural = "контакты"

    def __str__(self):
        return "Контакты"


class Address(models.Model):
    city = models.CharField("город", max_length=32, unique=True)
    address = models.CharField("адрес", max_length=64)

    caption = models.CharField("подпись", max_length=64)

    weekdays = models.CharField("режим работы по будням", max_length=48)
    weekends = models.CharField("режим работы по выходным", max_length=48)

    phone = PhoneField("номер телефона")

    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name="addresses", default=1)

    coordinates = models.CharField("координаты", max_length=32, null=True)

    class Meta:
        verbose_name = "адрес"
        verbose_name_plural = "адреса"

    def __str__(self):
        return f"{self.city} {self.address}"


class AdditionalPhone(models.Model):
    caption = models.CharField("подпись телефона", max_length=64)
    value = PhoneField("номер телефона")
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name="phones")

    def __str__(self):
        return f"{self.caption} - {self.value}"


class AdditionalEmail(models.Model):
    caption = models.CharField("подпись email", max_length=64)
    value = models.EmailField("email")
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name="emails")

    def __str__(self):
        return f"{self.caption} - {self.value}"


# requisites
class Requisite(models.Model):
    name = models.CharField("название организации", max_length=128)

    class Meta:
        verbose_name = "реквизиты"
        verbose_name_plural = "реквизиты"

    def __str__(self):
        return self.name


class RequisiteItem(models.Model):
    name = models.CharField("название", max_length=32, unique=True)
    value = models.CharField("значение", max_length=128)
    organization = models.ForeignKey(Requisite, on_delete=models.PROTECT, related_name="requisites", default=1)

    class Meta:
        verbose_name = "элемент реквизитов"
        verbose_name_plural = "элементы реквизитов"

    def __str__(self):
        return self.name
