from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('qr-code/', include('qr_code.urls', namespace="qr_code")),
    path('', include('fiscalizacao.urls')),
    path('api/', include('API.urls')),
    path('django-admin/', admin.site.urls),    
]
