from django.db import models
#
from model_utils.models import TimeStampedModel
#
from django.conf import settings
# Create your models here.


class AuditLog(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField('Action', max_length=255)
    ip_address = models.GenericIPAddressField('IP', null=True, blank=True)


    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = "Logs"
        ordering = ['user']
    

    def __str__(self):
        return f'{self.user} {self.action}'
