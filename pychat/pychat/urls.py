
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from room.views import RoomListViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register("api/room/select", RoomListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/schema/ui/', SpectacularSwaggerView.as_view()),
] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
