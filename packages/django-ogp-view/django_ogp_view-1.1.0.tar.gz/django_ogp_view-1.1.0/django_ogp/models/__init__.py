

from .masters import OgpLocaleMaster, OgpMimeTypeMaster
from .properties import (OgpBasicProperty, OgpCustomProperty, OgpMediaProperty,
                         OgpSiteProperty)

__all__ = [
    'OgpLocaleMaster',
    'OgpMimeTypeMaster',
    'OgpSiteProperty',
    'OgpMediaProperty',
    'OgpBasicProperty',
    'OgpCustomProperty',
]


def create_master(*args, **kwargs):
    classes = (OgpLocaleMaster, OgpMimeTypeMaster)
    for cls in classes:
        cls.create_master()
