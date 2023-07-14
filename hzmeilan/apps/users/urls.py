from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('users/', views.UserCreateAPIView.as_view())
]
