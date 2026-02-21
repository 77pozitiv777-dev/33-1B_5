from rest_framework.views import APIView
from urllib3 import request
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView

from apps.product.models import Product
from apps.product.serializers import ProductSerializer, ProductDetailSerializer, ProductCreateSerializer

serializer = ProductSerializer(data=request.data)

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

class ProductListAPIView(APIView):
    def get(self, request):
        cache_key = "product_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            # print("\n\n\n\nCache\n\n\n\n")
            return Response(cached_data, status=status.HTTP_200_OK)

        # print("\n\n\n\nDB\n\n\n\n")

        products = (
            Product.objects
            .select_related("category", "model")
            .prefetch_related("images")
            .order_by("-created_at")
        )
        serializer = ProductSerializer(products, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 2)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailAPIView(APIView):
    
    def get_object(self, uuid):
        return get_object_or_404(
            Product.objects.select_related("category", "model")
            .prefetch_related("images"), uuid=uuid
        )

    def get(self, request, uuid):
        serializer = ProductDetailSerializer(self.get_object(uuid))
        return Response(serializer.data)
    
    def put(self, request, uuid):
        product = self.get_object(uuid)
        serializer = ProductDetailSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            cache.delete("product_list")
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
        
    def patch(self, request, uuid):
        product = self.get_object(uuid)
        serializer = ProductDetailSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            cache.delete("product_list")
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, uuid):
        self.get_object(uuid).delete()
        cache.delete("product_list")
        return Response(status=204)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.select_related('category').all()

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

from rest_framework import mixins, generics
from .models import Category, Models
from .serializers import CategorySerializer, ModelsSerializer

# --- CRUD для Категорий ---

class CategoryListCreateAPIView(mixins.ListModelMixin, 
        mixins.CreateModelMixin, 
        generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryDetailAPIView(mixins.RetrieveModelMixin, 
        mixins.UpdateModelMixin, 
        mixins.DestroyModelMixin, 
        generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ModelsListCreateAPIView(mixins.ListModelMixin, 
        mixins.CreateModelMixin, 
        generics.GenericAPIView):
    queryset = Models.objects.all()
    serializer_class = ModelsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ModelsDetailAPIView(mixins.RetrieveModelMixin, 
        mixins.UpdateModelMixin, 
        mixins.DestroyModelMixin, 
        generics.GenericAPIView):
    queryset = Models.objects.all()
    serializer_class = ModelsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)