from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('login/', views.login_page,  name="login_page"),
    path('logout/', views.logout_user,  name="logout_user"),
    path('register/', views.register_page,  name="register_page"),

    path('tag/<int:pk>/edit/', views.tag_edit, name="tag_edit"),
    path('tag/<int:pk>/delete/', views.tag_delete, name="tag_delete"),
    path('tag/<int:pk>/add_card/', views.add_card, name="add_card"),

    path('card/<int:pk>/detail/', views.card_detail, name="card_detail"),
    path('card/<int:pk>/edit/', views.card_edit, name="card_edit"),
    path('card/<int:pk>/delete/', views.card_delete, name="card_delete"),


    path('task/<int:pk>/doing/', views.task_doing, name="task_doing"),
    path('task/<int:pk>/done/', views.task_done, name="task_done"),
    path('task/<int:pk>/delete/', views.task_delete, name="task_delete"),
    path('task/<int:pk>/edit/', views.task_edit, name="task_edit"),
]

