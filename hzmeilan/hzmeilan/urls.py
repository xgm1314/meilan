"""hzmeilan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(

    openapi.Info(

        title="美蓝",

        default_version='v1',

        description="美蓝医药API接口",

        # terms_of_service="https://www.google.com/policies/terms/",# 条款

        contact=openapi.Contact(email="177818396@qq.com"),  # 联系方式

        # license=openapi.License(name="BSD License"),# 许可证

    ),

    public=True,

    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ckeditor/', include('ckeditor_uploader.urls')),  # 富文本编辑器

    path('docs/', include_docs_urls(title='美蓝', description='')),

    # path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', include('apps.users.urls')),  # 用户模型
    path('', include('apps.verifications.urls')),  # 短信验证码
    path('', include('apps.oauth.urls')),  # qq第三方登录
    path('', include('apps.areas.urls')),  # 省市区
    path('', include('apps.goods.urls')),  # 商品
    path('', include('apps.carts.urls')),  # 购物车
    path('', include('apps.orders.urls')),  # 购物车
    path('', include('apps.payment.urls')),  # 购物车
]
