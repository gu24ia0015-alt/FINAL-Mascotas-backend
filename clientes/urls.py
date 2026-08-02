from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, MascotaViewSet

router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('mascotas', MascotaViewSet)

urlpatterns = router.urls