from django.urls import path
from .views import login, logout, get_user_info, validate_session

urlpatterns = [
    path('login/', login, name='api_login'),
    path('logout/', logout, name='api_logout'),
    path('user/', get_user_info, name='api_user_info'),
    path('validate/', validate_session, name='api_validate_session'),
]