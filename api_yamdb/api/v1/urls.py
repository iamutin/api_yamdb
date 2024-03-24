from django.urls import include, path
from rest_framework import routers

from .views import CreateUserView, TokenObtainView, UsersViewSet

v1_router = routers.DefaultRouter()

v1_router.register('users', UsersViewSet)

auth_urls = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('token/', TokenObtainView.as_view(), name='token'),
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(auth_urls)),
]
