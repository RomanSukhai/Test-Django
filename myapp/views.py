from rest_framework import viewsets, status
from .models import Product, Order, User
from .serializers import ProductSerializer, OrderSerializer, CustomUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        user_id = request.data.get('user')
        quantity = request.data.get('quantity')
        try:
            product = Product.objects.get(pk=product_id)
            user = User.objects.get(pk=user_id)
        except Product.DoesNotExist:
            return Response({"error": "Продукт не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({"error": "Кількість має бути цілим числом"}, status=status.HTTP_400_BAD_REQUEST)

        if product.stock >= quantity:
            product.stock -= quantity
            product.save()
            user.save()
            return super().create(request, *args, **kwargs)
        else:
            return Response({"error": "Недостатня кількість товару на складі"}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIRootView(APIView):
    """
    Кореневий API View, який надає гіперпосилання на основні ресурси.
    """

    def get(self, request, format=None):
        return Response({
            'products': reverse('product-list', request=request, format=format),
            'orders': reverse('order-list', request=request, format=format),
            'users': reverse('user-list', request=request, format=format)
        })

    def post(self, request, format=None):
        return Response({
            'products': reverse('product-list', request=request, format=format),
            'orders': reverse('order-list', request=request, format=format),
            'users': reverse('user-list', request=request, format=format)
        })