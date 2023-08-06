from django.shortcuts import render
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog


def index(request):
    return render(request, 'base_template/base.html', {
        "title": "Base Template",
        "breadcrumb": [
            {"title": "Home", "url": "/"}
        ]
    })


urlpatterns = [
    path('', index),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
