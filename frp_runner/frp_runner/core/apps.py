from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = 'frp_runner.frp_runner.core'
    label = 'core'
    verbose_name = _('Frp Manager')
