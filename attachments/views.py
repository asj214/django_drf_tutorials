from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from .models import Attachment
from .renderers import AttachmentRenderer
from .serializers import AttachmentSerializer


MEDIA_ROOT = settings.MEDIA_ROOT

# 실제 파일을 저장할 경로 및 파일 명 생성
# 폴더는 일별로 생성됨
def file_upload_path( filename):
    ext = filename.split('.')[-1]
    d = datetime.datetime.now()
    filepath = d.strftime('%Y\\%m\\%d')
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = "%s_%s.%s"%(uuid.uuid4().hex, suffix, ext)
    return os.path.join(MEDIA_ROOT , filepath, filename)


class CreateAttachmentApiView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AttachmentRenderer,)
    serializer_class = AttachmentSerializer
    # parser_classes = (FileUploadParser, MultiPartParser, FormParser)

    def post(self, request):

        params = {
            'attachmentable_type': request.data['attachmentable_type'],
            'attachment_id': request.data['attachment_id']
        }

        # print(request.data)
        # print(request.FILES)
        # file_name = request.data['file_name']

        return Response({'root': MEDIA_ROOT})
    
    
class DestroyAttachmentApiView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AttachmentRenderer,)
    serializer_class = AttachmentSerializer

    def delete(self, request):
        return Response({'msg': 'delete'})