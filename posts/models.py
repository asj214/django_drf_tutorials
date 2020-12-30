from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from system.models import BaseModel, SoftDeleteModel


class Post(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.DO_NOTHING,
        # db_index=False,
        db_constraint=False
    )
    title = models.CharField(verbose_name=_('title'), max_length=75)
    body = models.TextField()

    class Meta:
        db_table = 'posts'
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-created_at', '-updated_at']
        indexes = [
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return self.name