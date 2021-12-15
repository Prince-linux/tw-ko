from django.urls import path 

from . import views 


urlpatterns = [
    path("boards/", views.board_list_create, name="boards"),  # GET, POST
    path('boards/<int:pk>/', views.board_detail, name = 'board-detail'),
]
