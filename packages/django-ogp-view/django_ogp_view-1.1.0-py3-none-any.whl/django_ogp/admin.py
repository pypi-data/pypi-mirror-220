from django.contrib import admin
from django_ogp import models

admin.site.register(models.OgpLocaleMaster, ordering=('name',))
admin.site.register(models.OgpMimeTypeMaster, ordering=('name',))

admin.site.register(models.OgpSiteProperty, ordering=('name',))
admin.site.register(models.OgpMediaProperty, ordering=('url',))
admin.site.register(models.OgpBasicProperty, ordering=('url',))
admin.site.register(models.OgpCustomProperty, ordering=('url',))
