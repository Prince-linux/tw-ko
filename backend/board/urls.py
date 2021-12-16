from django.urls import path 

from . import views 


urlpatterns = [
    path("boards/", views.board_list_create, name="boards"),  # GET, POST
    path('boards/<int:pk>/', views.board_detail, name = 'board-detail'),
    path('boards/attachment/', views.attachment_create, name='board-attachment'),
    path('boards/attachment/<int:pk>/', views.attachment_detail, name='board-attachment-detail'),
]
