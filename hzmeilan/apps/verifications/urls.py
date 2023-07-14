from django.urls import path, re_path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'mobile/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeAPIView.as_view())
]
