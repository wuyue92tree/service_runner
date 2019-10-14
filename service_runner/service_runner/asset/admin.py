from django.contrib import admin
from django import forms
from django.db import models
from .models import Host, HostGroup, SshKey
# Register your models here.


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('ip', 'host_group', 'ssh_user',
                    'system_type', 'status', 'valid', 'update_time', 'create_time')
    list_filter = ('status', 'valid', 'host_group', 'system_type')
    list_editable = ('valid',)
    search_fields = ('ip', 'description')


@admin.register(SshKey)
class SshKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ssh_key')
    search_fields = ('name',)


@admin.register(HostGroup)
class HostGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
