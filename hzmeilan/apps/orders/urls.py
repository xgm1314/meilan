from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('order/settlement/', views.OrderSettlementAPIView.as_view()),  # 去结算
    path('order/', views.CommitOrderCreateAPIView.as_view()),  # 订单提交
]
