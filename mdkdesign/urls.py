from django.urls import path

from . import views





urlpatterns = [
    path('', views.mdkHome, name='mdkHome'),

]