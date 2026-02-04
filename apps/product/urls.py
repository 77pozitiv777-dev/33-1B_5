from django.urls import path
from apps.product.views import ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name='product-list'),
    path("products/<uuid:uuid>/", ProductDetailAPIView.as_view(), name='product-detail'),
    path("products/create/", ProductCreateAPIView.as_view(), name='create')
]