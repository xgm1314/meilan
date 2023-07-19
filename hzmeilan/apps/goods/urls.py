from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('categories/<int:pk>/skus/', views.SKUGenericAPIView.as_view()),
    path('categorys/<int:pk>/skus/', views.CategoryGenericAPIView.as_view()),

]
