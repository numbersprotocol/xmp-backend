import io
import json
import logging
import sys
import mimetypes

from django.http import HttpResponse, FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import pyxmp

from apps.injection.serializer import InjectionSerializer
from utils import external_api


logger = logging.getLogger(__name__)


class CreateInjectionView(APIView):
    """
    View to inject XMp metadata to image.

    * Requires token authentication.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="Create an XMP injected image",
        operation_description="""
        Inject the provided meta to the XMP metadata of the image.
        
        Set `send_to_external` as `True` to send the injected image and caption to predefined external API.
        
        The response is the injected image file.
        """,
        request_body=InjectionSerializer,
        responses={
            200: openapi.Response('File Attachment', schema=openapi.Schema(type=openapi.TYPE_FILE))
        },
    )
    def post(self, request, format=None):
        """
        Return an image injected with XMP metadata.
        """
        serializer = InjectionSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            information = json.loads(
                serializer.validated_data['meta']).get('information')
            xmp_image = pyxmp.inject(
                file.read(),
                information,
                'http://numbersprotocol.io/ns/starling/',
                'starling'
            )
            caption = serializer.validated_data.get('caption', '')

            # Send to external API
            if serializer.validated_data.get('send_to_external'):
                external_api.upload(xmp_image, file.name, caption)

            # Return the XMP image in response
            buffer = io.BytesIO(xmp_image)
            buffer.seek(0)
            content_type = mimetypes.guess_type(file.name)[0]
            response = FileResponse(
                buffer, content_type=content_type, as_attachment=True, filename=file.name)
            return response
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)
