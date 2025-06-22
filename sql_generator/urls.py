from django.contrib import admin
from django.urls import path, include
from authentication.views import login_page, dashboard_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/query/', include('query_engine.urls')),
    path('', login_page, name='home'),
    path('login/', login_page, name='login'),
    path('dashboard/', dashboard_page, name='dashboard'),
]