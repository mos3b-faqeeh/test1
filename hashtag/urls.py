from django.urls import path

from . import views





urlpatterns = [
    path('hashtagTracker', views.hashtagTracker, name='hashtagTracker'),

]