
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ogp.enums import Determiner, MediaType, OgpType
from django_ogp.models.masters import OgpLocaleMaster, OgpMimeTypeMaster


class OgpSitePropertyAbstract(models.Model):
    """Common property in all pages. unique info for each user.
    """
    name = models.CharField(
        verbose_name=_('name'),
        max_length=256,
        help_text='My Site Name')

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        abstract = True
        verbose_name = _('site property')
        verbose_name_plural = _('site properties')
        db_table = 'django_ogp_ogpsiteproperty'


class OgpSiteProperty(OgpSitePropertyAbstract):
    """Swappable common property.
    """

    class Meta(OgpSitePropertyAbstract.Meta):
        swappable = 'OGP_SITE_PROPERTY_MODEL'


class OgpMediaProperty(models.Model):
    """Media property for image, video, audio.
        ***** if media_type is audio, use only url, secure_url, type *****
    """
    media_type = models.CharField(
        verbose_name=_('media type'),
        max_length=16,
        choices=MediaType.choices)
    url = models.URLField(
        verbose_name=_('media url'),
        max_length=256,
        help_text='http://example.com/static/image/example.png')
    secure_url = models.URLField(
        verbose_name=_('media secure url'),
        max_length=256,
        null=True,
        blank=True,
        default=None,
        help_text='https://example.com/static/image/example.png')
    type = models.ForeignKey(
        OgpMimeTypeMaster,
        verbose_name=_('mime type'),
        on_delete=models.PROTECT)
    alt = models.CharField(
        verbose_name=_('media description'),
        max_length=256,
        help_text='Example Image')
    width = models.FloatField(
        verbose_name=_('media width [px]'),
        default=0,
        help_text=_('0 is not generate.'),
        validators=(MinValueValidator(0),))
    height = models.FloatField(
        verbose_name=_('media height [px]'),
        default=0,
        help_text=_('0 is not generate.'),
        validators=(MinValueValidator(0),))

    def __str__(self):
        return f'{self.media_type}: {self.url}'

    class Meta:
        verbose_name = _('media property')
        verbose_name_plural = _('media properties')
        db_table = 'django_ogp_ogpmediaproperty'


class OgpBasicProperty(models.Model):

    site = models.ForeignKey(
        OgpSiteProperty,
        verbose_name=_('site info'),
        on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name=_('title'),
        max_length=256,
        help_text='Test Page')
    type = models.CharField(
        verbose_name=_('type'),
        max_length=32,
        choices=OgpType.choices)
    url = models.URLField(
        verbose_name=_('site url'),
        max_length=256,
        help_text='http://example.com/test')

    description = models.CharField(
        verbose_name=_('description'),
        max_length=256,
        help_text='This is Test Page.',
        blank=True,
        null=True)
    determiner = models.CharField(
        verbose_name=_('type'),
        max_length=4,
        choices=Determiner.choices,
        blank=True,
        null=True)
    locales = models.ManyToManyField(
        OgpLocaleMaster,
        verbose_name=_('locales'),
        related_name='basics',
        blank=True)
    medias = models.ManyToManyField(
        OgpMediaProperty,
        verbose_name=_('medias'),
        related_name='basics',
        blank=True)

    def __str__(self):
        return f'{self.site.name}: {self.url}'

    class Meta:
        verbose_name = _('basic property')
        verbose_name_plural = _('basic properties')
        db_table = 'django_ogp_ogpbasicproperty'


class OgpCustomProperty(models.Model):

    site = models.ForeignKey(
        OgpSiteProperty,
        verbose_name=_('site info'),
        on_delete=models.CASCADE)
    type = models.CharField(
        verbose_name=_('type'),
        max_length=32,
        choices=OgpType.choices)
    url = models.URLField(
        verbose_name=_('site url'),
        max_length=256,
        help_text='http://example.com/test')

    property = models.JSONField(
        verbose_name=_('property'),
        help_text='{"book:author": "Test User", "book:tag": "novel"}')

    def __str__(self):
        return f'{self.site.name}: {self.url}'

    class Meta:
        verbose_name = _('custom property')
        verbose_name_plural = _('custom properties')
        db_table = 'django_ogp_ogpcustomproperty'
