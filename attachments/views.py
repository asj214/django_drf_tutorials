from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import server_error
from rest_framework.permissions import IsAuthenticated
from .models import Attachment
from .renderers import AttachmentRenderer
from .serializers import AttachmentSerializer
from django.contrib.contenttypes.models import ContentType
from system.common import (
    make_filename,
    s3_upload_from_obj,
    s3_delete
)


class CreateAttachmentApiView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AttachmentRenderer,)
    serializer_class = AttachmentSerializer

    def post(self, request):

        upfile = request.FILES.get('upfile')
        path = 'sjahn/images/{0}'.format(make_filename(upfile.name))
        res = s3_upload_from_obj(upfile, path)

        if res.get('path') is None:
            return server_error()

        attachmentable = ContentType.objects.get(model=request.data.get('attachmentable_type'))
        serializer_context = {'user': request.user, 'request': request}
        serializer_data = {
            'attachmentable_type': attachmentable.id,
            'attachmentable_id': request.data.get('attachmentable_id'),
            'name': upfile.name,
            'path': path
        }

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class DestroyAttachmentApiView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AttachmentRenderer,)
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects

    def delete(self, request, pk=None):
        attachment = self.queryset.filter(pk=pk).first()

        if attachment is not None:
            res = s3_delete(attachment.path)
            attachment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
