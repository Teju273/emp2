from django.urls import path, include
from rest_framework.routers import DefaultRouter

from emp import views


router = DefaultRouter()
router.register('user-detail', views.EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login, name='login')

]
