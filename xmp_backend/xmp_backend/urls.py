"""xmp_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from apps.injection.views import CreateInjectionView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


schema_view = get_schema_view(
    openapi.Info(
        title="XMP Injection API",
        default_version='v1',
        description="""
        XMP Injection API
        
        # Authentication
        
        Authentication header must include the literal text `token` as prefix.
        
        Example: `{ "Authorization": "token <the-actual-token>" }`
        
        # Meta example
        
        ```
        {
            "proof":{
                "hash":"b08714406df079733fdbc0566aa28ff4b20abd13e3a2042ddd214bc4d4f81f7c",
                "mimeType":"image/jpeg",
                "timestamp":1600177819743
            },
            "information":[
                {
                    "provider": "InfoSnapshot",
                    "name": "Brand",
                    "value": "My Service"
                },
                {
                    "provider": "InfoSnapshot",
                    "name": "Current GPS Accuracy",
                    "value": "14.589"
                },
                {
                    "provider": "InfoSnapshot",
                    "name": "Current GPS Latitude",
                    "value": "25.045234"
                },
                {
                    "provider": "InfoSnapshot",
                    "name": "Current GPS Longitude",
                    "value": "121.530795"
                },
                {
                    "provider": "InfoSnapshot",
                    "name": "Current GPS Timestamp",
                    "value": "2020-09-15T13:50:25.143Z"
                },
                {
                    "provider":"InfoSnapshot",
                    "name":"Timestamp",
                    "value":"2020-09-15T13:50:30.203Z"
                }
            ]
        }
        ```
        """,
        contact=openapi.Contact(email="hi@numbersprotocol.io"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('injection/', CreateInjectionView.as_view(), name='injection'),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    url(r'^redoc/$', schema_view.with_ui(
        'redoc',
        cache_timeout=0), name='schema-redoc'),
]
urlpatterns += staticfiles_urlpatterns()
