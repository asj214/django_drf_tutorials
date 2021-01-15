from django.db import models
from django.conf import settings
from system.models import BaseModel


class Reference(BaseModel):
    name = models.CharField(verbose_name='name', max_length=75, help_text='그룹 네임')
    key = models.CharField(verbose_name='key', max_length=75)
    value = models.CharField(verbose_name='value', max_length=75)
    order = models.IntegerField(verbose_name='order', default=0, help_text='100 단위씩 끊어서 그룹화')

    class Meta:
        db_table = 'references'
        ordering = ['name', 'order', '-created_at']
        indexes = [
            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name', 'key', 'value'], name='unique_columns')
        ]

    def __str__(self):
        return self.name