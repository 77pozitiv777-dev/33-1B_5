from django.urls import path
from apps.product.views import ProductListAPIView
from apps.product.utils import ProductDetailAPIView

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name='product-list'),
    path("products/<uuid:uuid>/", ProductDetailAPIView.as_view(), name='product-detail'),
]
