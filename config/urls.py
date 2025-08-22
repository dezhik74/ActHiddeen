from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('', include('hiddenactsbase.urls')),
    path('admin/', admin.site.urls, name='admin_url'),
    ]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# При разработке приложения для обслуживания файлов media
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
