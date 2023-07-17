from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('qq/oauth/', views.QQOauthURLAPIView.as_view()),  # 拼接QQ登录的url
    path('qq/users/', views.OauthQQAPIView.as_view()),  # 绑定openid

]
