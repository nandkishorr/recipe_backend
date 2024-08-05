from django.urls import path
from auth.views import MyObtainTokenPairView,RegisterView,UserDeleteView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),

]