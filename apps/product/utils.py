from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.product.models import Product
from apps.product.serializers import ProductSerializer

class ProductDetailAPIView(APIView):
    def get(self, request, uuid):
        try:
            product = (Product.objects.select_related("category", "model")
            .prefetch_related("images").get(uuid=uuid))
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)