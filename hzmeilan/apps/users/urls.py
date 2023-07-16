from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('users/', views.UserCreateAPIView.as_view()),  # 用户注册
    path('jwtlogin/', obtain_jwt_token),  # 用户登录
    path('users/<pk>/', views.UserRetrieveAPIView.as_view()),  # 用户详情页面
]
