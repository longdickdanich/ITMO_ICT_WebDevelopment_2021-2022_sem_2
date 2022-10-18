from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

import magic
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat


class Admin(AbstractUser):
    phone = models.CharField(max_length=14)
    full_name = models.CharField(max_length=255)


class Room(models.Model):
    name = models.CharField(verbose_name="Название номера", max_length=255)
    number = models.IntegerField(verbose_name="номер", )
    floor = models.IntegerField(verbose_name="этаж", )
    cost_of_living = models.IntegerField(verbose_name="цена заселения", )
    ROOM_TYPES = [(1, "Одноместный"), (2, "Двуместный"), (3, "Трёхместный")]
    room_type = models.IntegerField(verbose_name="тип комнаты", choices=ROOM_TYPES)


class Client(models.Model):
    full_name = models.CharField(verbose_name="имя", max_length=255)
    pasport = models.CharField(verbose_name="паспорт", max_length=20)
    city = models.CharField(verbose_name="город", max_length=255)
    rooms = models.ManyToManyField(to=Room, through='Inhabitation')


class Inhabitation(models.Model):
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, verbose_name="Комната", on_delete=models.SET_NULL, null=True)
    in_date = models.DateField(verbose_name="Дата заселения", )
    out_date = models.DateField(verbose_name="Дата выселения", )


class Cleaner(models.Model):
    full_name = models.CharField(verbose_name="ФИО", max_length=255)
    phone = models.CharField(verbose_name="Телефон", max_length=14)
    contract_number = models.CharField(verbose_name="Договор", max_length=255)
    old_phone = models.CharField(verbose_name="Старый телефон", max_length=14, blank=True, default="")

    def __str__(self):
        return self.full_name

    # def __init__(self, *args, **kwargs):
    #     super(Cleaner, self).__init__(*args, **kwargs)
    #     self.old_phone_tmp = self.phone
    #
    # def save(self, **kwargs):
    #     # print("Some logic")
    #     self.old_phone = self.old_phone_tmp
    #     super().save(**kwargs)


class CleanerAvatar(models.Model):
    file = models.ImageField()
    file_name = models.CharField(max_length=255)
    file_size = models.FloatField()
    cleaner = models.ForeignKey(to=Cleaner, on_delete=models.CASCADE)


class Cleaning(models.Model):
    cleaner = models.ForeignKey(Cleaner,on_delete=models.SET_NULL, null=True)
    cleaning_floor = models.IntegerField()
    cleaning_day = models.DateField()


@deconstructible
class FileValidator(object):
    error_messages = {
        'max_size': ("Ensure this file size is not greater than %(max_size)s."
                     " Your file size is %(size)s."),
        'min_size': ("Ensure this file size is not less than %(min_size)s. "
                     "Your file size is %(size)s."),
        'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                  'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'],
                                  'min_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'],
                                      'content_type', params)

    def __eq__(self, other):
        return (
                isinstance(other, FileValidator) and
                self.max_size == other.max_size and
                self.min_size == other.min_size and
                self.content_types == other.content_types
        )


file_validator = FileValidator(max_size=1024 * 100,
                               content_types=("image/jpeg",))


class FileUploads(models.Model):
    file = models.FileField(validators=[file_validator])
