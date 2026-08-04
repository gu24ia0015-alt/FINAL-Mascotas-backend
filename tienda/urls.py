from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, PedidoViewSet

router = DefaultRouter()
router.register('productos', ProductoViewSet)
router.register('pedidos', PedidoViewSet)

urlpatterns = router.urls