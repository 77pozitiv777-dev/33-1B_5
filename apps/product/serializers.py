from rest_framework import serializers
from apps.product.models import Category, Models, Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

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
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            "id",
            "uuid",
            "title",
            "description",
            "price",
            "images",
            "category"
        ]
    class Meta:
        model = Product
        fields = '__all__'