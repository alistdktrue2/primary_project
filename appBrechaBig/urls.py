
from django.contrib import admin
from django.urls import path
from appBrecha.views import home_view,register_view,login_view,dashboard_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",home_view, name='home_view'),
    path('signup/',register_view, name='register_view'),
    path('signin/',login_view, name='signin'),
    path('dashboard/',dashboard_view, name='dashboard_view'),
]
