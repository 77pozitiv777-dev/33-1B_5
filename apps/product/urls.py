from django.urls import path, include
from apps.product.views import ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name='product-list'),
    path("products/<uuid:uuid>/", ProductDetailAPIView.as_view(), name='product-detail'),
    path("products/create/", ProductCreateAPIView.as_view(), name='create'),
    path('', include(router.urls)),
]