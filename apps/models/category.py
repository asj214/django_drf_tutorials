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
    user = models.ForeignKey(
        'apps.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False
    )
    name = models.CharField(max_length=50)
    depth = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['depth', 'order']
    
    def __str__(self):
        return '{}: {}'.format(self.id, self.name)