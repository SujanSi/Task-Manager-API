from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update-task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete-task'),
]