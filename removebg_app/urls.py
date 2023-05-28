from django.urls import path
from .views import FastRemove,SlowRemove

urlpatterns = [
    path('fast_remove/',FastRemove.as_view(),name = 'fast_remove'),
    path('slow_remove/',SlowRemove.as_view(),name = 'slow_remove'),
]