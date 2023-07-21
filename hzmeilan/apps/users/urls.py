from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('users/', views.UserCreateAPIView.as_view()),  # 用户注册
    path('jwtlogin/', obtain_jwt_token),  # 用户登录
    path('users/<pk>/', views.UserRetrieveAPIView.as_view()),  # 用户详情页面
    path('emails/<int:pk>/', views.EmailUpdateAPIView.as_view()),  # 用户邮箱修改
    path('emails/verification/', views.EmailActivationAPIView.as_view()),  # 用户邮箱激活
    path('browser_history/', views.UserBrowserHistoryCreateAPIView.as_view()),  # 用户浏览记录
]
router = DefaultRouter()
router.register(prefix='addresses', viewset=views.AddressGenericViewSet, basename='addresses')
urlpatterns += router.urls
