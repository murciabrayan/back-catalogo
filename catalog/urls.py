from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AdditionalOptionViewSet,
    AdminDashboardView,
    AdminLoginView,
    AdminMeView,
    AdminPasswordChangeView,
    ProductViewSet,
    PublicProductListAPIView,
)

router = DefaultRouter()
router.register('admin/products', ProductViewSet, basename='admin-products')
router.register('admin/additional-options', AdditionalOptionViewSet, basename='admin-additional-options')

urlpatterns = [
    path('catalog/products/', PublicProductListAPIView.as_view(), name='public-products'),
    path('auth/login/', AdminLoginView.as_view(), name='admin-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', AdminMeView.as_view(), name='admin-me'),
    path('auth/change-password/', AdminPasswordChangeView.as_view(), name='admin-change-password'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('', include(router.urls)),
]
