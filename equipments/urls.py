# from .views import equipment_stats_view
from django.urls import path, include
# from .admin import CustomAdminSite
from django.contrib import admin

# custom_admin_site = CustomAdminSite()
# custom_admin_site.discover_apps()  # <- Nếu bạn dùng autodiscovery

urlpatterns = [
    # path('custom-admin/', custom_admin_site.urls),  # Admin có dashboard biểu đồ
    # path('equipment-stats/', equipment_stats_view, name='equipment_stats'),
]
