from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('carts/', views.CartsAPIView.as_view()),  # 购物车增删改查
    path('carts/selection/', views.CartSelectedAllAPIView.as_view()),  # 购物车全选

]
