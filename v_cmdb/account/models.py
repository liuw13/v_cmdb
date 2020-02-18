from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('1', u'总监'),
        ('2', u'经理'),
        ('3', u'研发'),
    )
    role = models.CharField(max_length=32, default='developer', choices=ROLES)
    remark = models.CharField(max_length=128, default='', blank=True)

    class Meta:
        verbose_name_plural = u'用户'

    def __unicode__(self):
        return self.username