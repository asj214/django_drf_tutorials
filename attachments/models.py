from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from system.models import BaseModel, SoftDeleteModel


class Attachment(BaseModel, SoftDeleteModel):
    
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.DO_NOTHING,
        # db_index=False,
        db_constraint=False
    )

    # attachment
    attachmentable_type = models.ForeignKey(
        ContentType,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        db_column='attachmentable_type'
    )
    attachmentable_id = models.PositiveIntegerField(
        default=None,
        null=True,
        db_column='attachmentable_id'
    )
    content_object = GenericForeignKey('attachmentable_type', 'attachmentable_id')
    name = models.CharField(null=False, max_length=200)
    path = models.CharField(null=False, max_length=200)

    class Meta:
        db_table = 'attachments'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['attachmentable_id', 'attachmentable_type', 'deleted_at']),
        ]

    def __str__(self):
        return self.name