from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('card/<int:pk>/detail/', views.card_detail, name="card_detail")
]
