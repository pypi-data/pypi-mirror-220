
import typing as typ

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ogp.enums import Locale, MimeType


class MasterAbstract(models.Model):
    name_choices_class: typ.Type[models.Choices] = models.Choices
    name_verbose_name = None

    name = models.CharField(
        verbose_name=name_verbose_name,
        primary_key=True,
        choices=name_choices_class.choices)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    @classmethod
    def create_master(cls):
        data = [cls(name=choice[0]) for choice in cls.name_choices_class.choices]
        return cls.objects.bulk_create(data, ignore_conflicts=True)


class OgpLocaleMaster(MasterAbstract):
    name_choices_class = Locale
    name_verbose_name = _('locale')

    name = models.CharField(
        verbose_name=name_verbose_name,
        primary_key=True,
        choices=name_choices_class.choices)

    class Meta:
        verbose_name = _('locale master')
        verbose_name_plural = _('locale masters')
        db_table = 'django_ogp_ogplocalemaster'
        swappable = 'OGP_LOCALE_MASTER_MODEL'


class OgpMimeTypeMaster(MasterAbstract):
    name_choices_class = MimeType
    name_verbose_name = _('mime type')

    name = models.CharField(
        verbose_name=name_verbose_name,
        primary_key=True,
        choices=name_choices_class.choices)

    class Meta:
        verbose_name = _('mime type master')
        verbose_name_plural = _('mime type masters')
        db_table = 'django_ogp_ogpmimetypemaster'
        swappable = 'OGP_MIMETYPE_MASTER_MODEL'
