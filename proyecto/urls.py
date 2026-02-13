from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from pages.urls import pages_patterns


urlpatterns = [
    # Core / Home
    path('', include('core.urls')),

    # Pages
    path('pages/', include(pages_patterns)),

    # Admin
    path('admin/', admin.site.urls),

    # Autenticación
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),

    # Apps
    path('contact/', include('contact.urls')),
    path('lectorqr/', include('lectorqr.urls')),
]

# ⚠️ MUY IMPORTANTE PARA MOSTRAR IMÁGENES EN DESARROLLO
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    
    





