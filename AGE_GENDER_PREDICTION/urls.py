from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^agegender/',include('app.urls')), # admin login
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

