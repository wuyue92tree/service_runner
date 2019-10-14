from django.contrib import admin
from django import forms
from django.db import models
from .models import Host, HostGroup, SshKey
# Register your models here.


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):


@admin.register(SshKey)
class SshKeyAdmin(admin.ModelAdmin):
    pass


@admin.register(HostGroup)
class HostGroupAdmin(admin.ModelAdmin):
    pass
