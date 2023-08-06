
import typing as typ

from django_ogp.enums import OgpType
from django_ogp.models import OgpBasicProperty, OgpCustomProperty


class OgpViewMixin:
    ogp_global_prefix = 'og: https://ogp.me/ns#'

    # site, type, url should be same for ogp, ogp_custom.
    # Other attributes are output as is if duplicate attributes exist.
    # if set to class variant, restart.
    ogp: typ.Optional[OgpBasicProperty] = None
    ogp_custom: typ.Optional[OgpCustomProperty] = None

    @property
    def ogp_prefix(self):
        prefix = list(filter(lambda v: v, [
            self.ogp and OgpType.get_namespace(self.ogp.type),
            self.ogp_custom and OgpType.get_namespace(self.ogp_custom.type),
        ]))

        return prefix[0] if prefix else ''
