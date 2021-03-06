from django.db import models
from configs.models import BaseModel


class Category(BaseModel):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='children'
    )
    user = models.ForeignKey(
        'apps.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False
    )
    name = models.CharField(max_length=50)
    depth = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'categories'
        ordering = ['depth', 'order']
    
    def __str__(self):
        return '{}: {}'.format(self.id, self.name)