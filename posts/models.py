from django.db import models
from system.models import BaseModel, SoftDeleteModel
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment


class Post(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.DO_NOTHING,
        # db_index=False,
        db_constraint=False
    )
    title = models.CharField(max_length=75)
    body = models.TextField()
    comments = GenericRelation(Comment, object_id_field='commentable_id', content_type_field='commentable_type')

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at', '-updated_at']
        indexes = [
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return self.name