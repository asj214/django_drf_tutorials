from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from system.models import BaseModel, SoftDeleteModel


class Comment(BaseModel, SoftDeleteModel):

    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.DO_NOTHING,
        # db_index=False,
        db_constraint=False
    )

    # commentable
    commentable_type = models.ForeignKey(
        ContentType,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        db_column='commentable_type'
    )
    commentable_id = models.PositiveIntegerField(
        default=None,
        null=True,
        db_column='commentable_id'
    )
    content_object = GenericForeignKey('commentable_type', 'commentable_id')
    body = models.TextField(null=False)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at', '-updated_at']
        # indexes = [
        #     models.Index(fields=['commentable_id', 'commentable_type', 'deleted_at']),
        # ]

    def __str__(self):
        return self.name