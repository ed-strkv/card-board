from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('card/<int:pk>/detail/', views.card_detail, name="card_detail"),
    path('task/<int:pk>/detail/', views.task_detail, name="task_detail"),
    path('add_tag/', views.add_tag, name="add_tag"),
    path('tag/<int:pk>/edit/', views.tag_edit, name="tag_edit"),
    path('tag/<int:pk>/delete/', views.tag_delete, name="tag_delete"),
    path('tag/<int:pk>/add_card/', views.add_card, name="add_card"),
    path('card/<int:pk>/edit/', views.edit_card, name="edit_card"),
]
