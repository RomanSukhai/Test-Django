from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Product, Order, User
from .serializers import ProductSerializer, OrderSerializer, CustomUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse


# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#
#     def create(self, request, *args, **kwargs):
#         product_id = request.data.get('product')
#         user_id = request.data.get('user')
#         quantity = request.data.get('quantity')
#         try:
#             product = Product.objects.get(pk=product_id)
#             user = User.objects.get(pk=user_id)
#         except Product.DoesNotExist:
#             return Response({"error": "Продукт не знайдено"}, status=status.HTTP_404_NOT_FOUND)
#         try:
#             quantity = int(quantity)
#         except (ValueError, TypeError):
#             return Response({"error": "Кількість має бути цілим числом"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if product.stock >= quantity:
#             product.stock -= quantity
#             product.save()
#             user.save()
#             return super().create(request, *args, **kwargs)
#         else:
#             return Response({"error": "Недостатня кількість товару на складі"}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def create_order(request):
    products = Product.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(Product, pk=product_id)

        try:
            quantity = int(quantity)
            if product.stock >= quantity:
                with transaction.atomic():
                    product.stock -= quantity
                    product.save()
                    order = Order(user=request.user, product=product, quantity=quantity)
                    order.save()
                messages.success(request, "Замовлення успішно створено.")
                return redirect('home')
            else:
                messages.error(request, "Недостатня кількість товару на складі.")
        except ValueError:
            messages.error(request, "Кількість має бути цілим числом.")

    return render(request, 'create_order.html', {'products': products})



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

@login_required
def home_view(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'home.html', context)


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user)
    return render(request, 'home.html', {'orders': orders})


def register(request):
    if request.method == 'POST':
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html')
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


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
