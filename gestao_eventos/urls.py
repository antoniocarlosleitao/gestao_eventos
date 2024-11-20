from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
#from django.views.static import serve

from gestao_eventos import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tipos.urls')),
]

if settings.DEBUG:
    #urlpatterns += [path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)