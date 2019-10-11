from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    client_dir = models.CharField(
        default='/opt/frp/bin/frpc', max_length=255, verbose_name=_('clientDir'))
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name=_('createTime'))
    update_time = models.DateTimeField(
        auto_now=True, verbose_name=_('updateTime'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Frp Client')
        verbose_name_plural = _('Frp Clients')


class ClientConfig(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name=_('Client'))
    content = models.TextField(verbose_name=_('Content'))
    valid = models.BooleanField(default=False, verbose_name=_('Valid'))
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name=_('createTime'))
    update_time = models.DateTimeField(
        auto_now=True, verbose_name=_('updateTime'))

    def __str__(self):
        return self.client.name

    class Meta:
        verbose_name = _('Client Config')
        verbose_name_plural = _('Client Configs')


class Server(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    server_dir = models.CharField(
        default='/opt/frp/bin/frps', max_length=255, verbose_name=_('serverDir'))
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name=_('createTime'))
    update_time = models.DateTimeField(
        auto_now=True, verbose_name=_('updateTime'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Frp Server')
        verbose_name_plural = _('Frp Servers')


class ServerConfig(models.Model):
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, verbose_name=_('Server'))
    content = models.TextField(verbose_name=_('Content'))
    valid = models.BooleanField(default=False, verbose_name=_('Valid'))
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name=_('createTime'))
    update_time = models.DateTimeField(
        auto_now=True, verbose_name=_('updateTime'))

    def __str__(self):
        return self.server.name

    class Meta:
        verbose_name = _('Server Config')
        verbose_name_plural = _('Server Configs')
