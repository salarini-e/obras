from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('qr-code/', include('qr_code.urls', namespace="qr_code")),
    path('', include('fiscalizacao.urls')),
    path('admin/', admin.site.urls),
]
