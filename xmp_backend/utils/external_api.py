import base64
import requests
import json

from django.conf import settings


def upload(file, filename, caption):
    upload_url = _get_signed_upload_url(
        settings.EXTERNAL_API_ENDPOINT,
        settings.EXTERNAL_API_KEY,
        filename,
        base64.b64encode(caption.encode('utf-8')),
    )
    resp = _upload_file(upload_url, file)


def _get_signed_upload_url(endpoint, api_key, filename, encoded_caption):
    headers = {
        'x-api-key': api_key,
        'x-amz-meta-filekey': filename,
        'memo': encoded_caption,
    }
    resp = requests.get(
        url=endpoint,
        headers=headers,
    )
    resp.raise_for_status()
    return resp.json()


def _upload_file(url, data):
    resp = requests.put(url=url, data=data)
    resp.raise_for_status()
    return resp
