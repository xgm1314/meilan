from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('areas/', views.AreasListAPIView.as_view()),  # 查询所有省
    # path('areas/<int:pk>/', views.AreasRetrieveAPIView.as_view()),  # 查询市区县
]
router = DefaultRouter()
router.register(prefix='areas', viewset=views.AreasReadOnlyModelViewSet, basename='areas')
urlpatterns += router.urls
