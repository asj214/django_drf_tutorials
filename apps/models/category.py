from django.db import models


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name='children'
    )
    name = models.CharField(max_length=50)
    depth = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'categories'
        ordering = ['parent__id', 'order']
        constraints = [
            models.UniqueConstraint(fields=['depth', 'name'], name='uniques')
        ]
    
    def __str__(self):
        return '{}: {}'.format(self.id, self.name)
