from django.urls import path
from django.conf.urls import include

from MrMilk import views
from rest_framework import routers

from MrMilk.views import ProductViewSet, BrandViewSet, OrderViewSet, OrderDetailViewSet, UserProfileViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'order', OrderViewSet)
router.register(r'order-detail', OrderDetailViewSet)
router.register(r'users', UserProfileViewSet)

app_name = 'Mr_Milk'
urlpatterns = [
    path('', include(router.urls), name='product_list'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
]
