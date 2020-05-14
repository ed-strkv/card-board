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
    path('card/<int:pk>/delete/', views.card_delete, name="card_delete"),

    #path('card/<int:pk>/add_task/', views.task_add, name="task_add"),
    path('task/<int:pk>/doing/', views.task_doing, name="task_doing"),
    path('task/<int:pk>/done/', views.task_done, name="task_done"),
    path('task/<int:pk>/delete/', views.task_delete, name="task_delete"),
    path('task/<int:pk>/edit/', views.edit_task, name="edit_task"),
    

]

