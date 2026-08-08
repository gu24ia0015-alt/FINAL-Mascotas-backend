from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, PedidoViewSet, CategoriaViewSet, ProveedorViewSet

router = DefaultRouter()
router.register('productos', ProductoViewSet)
router.register('pedidos', PedidoViewSet)
router.register('categorias', CategoriaViewSet)
router.register('proveedores', ProveedorViewSet)

urlpatterns = router.urls
