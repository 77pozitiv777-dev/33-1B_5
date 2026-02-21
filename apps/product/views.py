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

from django.core.mail import send_mail
from .models import PasswordResetCode
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                PasswordResetCode.objects.filter(email=email).delete()
                reset_obj = PasswordResetCode.objects.create(email=email)
                send_mail(
                    'Код для сброса пароля',
                    f'Ваш код подтверждения: {reset_obj.code}',
                    'noreply@myapp.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "Код отправлен на почту."}, status=status.HTTP_200_OK)
            return Response({"error": "Пользователь с такой почтой не найден."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            PasswordResetCode.objects.filter(email=email).delete()
            
            return Response({"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)