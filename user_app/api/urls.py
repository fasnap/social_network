from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user_app.api import views

urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.user_registration_view.as_view(), name='user-register'),
    # path('logout/', views.APILogoutView.as_view(), name='logout_token'),
]
