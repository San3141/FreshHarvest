from django.urls  import path
from rest_framework.routers import DefaultRouter

from . import farmer_views, order_views, review_views
from . import user_views
from . import product_views
from . import cart_views



router = DefaultRouter()
router.register('auth', user_views.AuthenticationViewSet)
router.register('products', product_views.ProductViewSet)
router.register('carts', cart_views.CartViewSet)
router.register('orders', order_views.OrderViewSet)
router.register('farmers', farmer_views.FarmerViewSet)
router.register('reviews', review_views.ReviewViewSet)
urlpatterns = router.urls