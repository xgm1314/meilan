from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('order/settlement/', views.OrderSettlementAPIView.as_view()),  # 去结算
    path('order/', views.CommitOrderCreateAPIView.as_view()),  # 订单提交
    path('order/list/', views.OrderListAPIView.as_view()),  # 订单查看
    path('order/delete/<pk>/', views.OrderDestroyAPIView.as_view()),  # 订单逻辑删除
    path('order/cancellation/', views.CancellationOrderUpdateAPIView.as_view()),  # 订单取消
]
