from django.contrib import admin
from frp_runner.frp_runner.core.models import *
from django.utils.translation import gettext_lazy as _
# Register your models here.


class ClientConfigTabularInline(admin.TabularInline):
    model = ClientConfig
    extra = 0


class ServerConfigTabularInline(admin.TabularInline):
    model = ServerConfig
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_dir',
                    'display_config_count', 'display_config_valid_count', 'create_time')
    search_fields = ('name', 'client_dir')
    inlines = (ClientConfigTabularInline,)

    def display_config_count(self, obj):
        return obj.clientconfig_set.count()

    display_config_count.short_description = _('Config Counts')

    def display_config_valid_count(self, obj):
        return obj.clientconfig_set.filter(valid=True).count()

    display_config_valid_count.short_description = _('Active Config Counts')


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'server_dir',
                    'display_config_count', 'display_config_valid_count', 'create_time')
    search_fields = ('name', 'server_dir')
    inlines = (ServerConfigTabularInline,)

    def display_config_count(self, obj):
        return obj.serverconfig_set.count()

    display_config_count.short_description = _('Config Counts')

    def display_config_valid_count(self, obj):
        return obj.serverconfig_set.filter(valid=True).count()

    display_config_valid_count.short_description = _('Active Config Counts')
