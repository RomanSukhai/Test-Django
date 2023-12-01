"""
URL configuration for DjangoProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home.html, name='home.html')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home.html')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers

from myapp.models import Product
from myapp.views import ProductViewSet, OrderViewSet, CustomUserViewSet, APIRootView, register, login_view,home
from rest_framework import permissions
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'users', CustomUserViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="API for my project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
admin.site.register(Product)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # path('', APIRootView.as_view(), name='api-root'),
    path('api/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]