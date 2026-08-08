from rest_framework.routers import DefaultRouter
from .views import CitaViewSet, VeterinarioViewSet, ServicioViewSet

router = DefaultRouter()
router.register('citas', CitaViewSet)
router.register('veterinarios', VeterinarioViewSet)
router.register('servicios', ServicioViewSet)

urlpatterns = router.urls
