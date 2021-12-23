from django.urls import path 

from . import views 


urlpatterns = [
    path("boards/", views.board_list_create, name="boards"),  # GET, POST
    path('boards/detail/<int:pk>/', views.board_detail, name = 'board-detail'),
    path('boards/attachment/', views.attachment_create, name='board-attachment'),
    path('boards/attachment/<int:pk>/', views.attachment_detail, name='board-attachment-detail'),
    path('boards/card/', views.card_create, name='board-card'),
    path('boards/card/<int:pk>/', views.card_detail, name='board-card-detail'),
    path("boards/list/", views.list_create, name="list-create"), 
    path('boards/list/<int:pk>/', views.list_detail, name='board-list-detail'),
]
