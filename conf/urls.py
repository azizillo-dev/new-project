from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_rooot=settings.MEDIA_ROOT)
