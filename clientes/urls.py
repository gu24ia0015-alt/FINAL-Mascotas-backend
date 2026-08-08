from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, MascotaViewSet, EspecieViewSet, DireccionViewSet

router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('mascotas', MascotaViewSet)
router.register('especies', EspecieViewSet)
router.register('direcciones', DireccionViewSet)

urlpatterns = router.urls
