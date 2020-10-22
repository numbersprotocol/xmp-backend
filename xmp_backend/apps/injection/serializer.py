import json
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from pyxmp import pyxmp


class RequirableBooleanField(serializers.BooleanField):
    default_empty_html = serializers.empty


class InjectionSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=255)
    meta = serializers.CharField()
    caption = serializers.CharField(required=False)
    send_to_external = RequirableBooleanField()
