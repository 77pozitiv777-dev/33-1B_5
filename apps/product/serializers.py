from rest_framework import serializers

from apps.product.models import Category, Models, Product, ProductImage
from lesson_1.apps import product

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "uuid",
            "title",
            "description",
            "price",
            "first_image"
        ]

    def get_first_image(self, obj):
        first_img = obj.images.first()
        if first_img:
            return first_img.image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)
    model_title = serializers.CharField(source='model.title', read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "uuid", "title", 
            "description", "price", 
            "created_at", "size", 
            "is_active", "is_favorite", 
            "images", "model_title", "category_title"
        ]

class ProductCreateSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'category', 'model', 'title', 'description', 
            'price', 'size', 'images', 'uploaded_images'
        ]

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Название должно быть минимум 3 символа!")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должно быть больше 0!")
        return value

    def validate_size(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Размер слишком длинный!")
        return value

    def validate(self, attrs):
        category = attrs.get("category")
        model = attrs.get("model")

        if model and category and model.category != category:
            raise serializers.ValidationError(
                "Модель не принадлежит выбранной категории!"
            )

        return attrs

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product

from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ModelsSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.title')

    class Meta:
        model = Models
        fields = '__all__'

from django.contrib.auth import get_user_model

User = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        from .models import PasswordResetCode
        reset_entry = PasswordResetCode.objects.filter(email=data['email'], code=data['code']).first()
        
        if not reset_entry:
            raise serializers.ValidationError("Неверный код или email.")
        return data