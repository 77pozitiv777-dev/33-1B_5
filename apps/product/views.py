from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from apps.product.models import Product
from apps.product.serializers import ProductSerializer

from rest_framework import generics

class ProductListAPIView(generics.ListAPIView):
    def get(self, request):
        cache_key = "product_list"
        cached_data = cache.get(cache_key)


        if cached_data:
            # print("\n\n\n\nCache\n\n\n\n")
            return Response(cached_data, status=status.HTTP_200_OK)
        
        # print("\n\n\n\nCache\n\n\n\n")

        products = (
            Product.objects
            .select_related("category", "model")
            .prefetch_related("images")
            .order_by("-created_at")
        )
        serializer_class = ProductSerializer(products, many=True)
        cache.set(cache_key, serializer_class.data, timeout=60 * 2)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.query_params.get('category')
        model_id = self.request.query_params.get('model')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if category:
            queryset = queryset.filter(category_id=category)
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset