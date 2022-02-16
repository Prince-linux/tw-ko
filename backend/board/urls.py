from django.urls import path

from . import views


urlpatterns = [
    path("boards/", views.board_list_create,
         name="boards"),  # LIST (GET), POST
    path('boards/<int:pk>/', views.board_detail,
         name='board-detail'),  # GET with id
    path('boards/attachment/', views.attachment_create, name='attachments'),
    path('boards/attachment/<int:pk>/',
         views.attachment_detail, name='attachment-detail'),
    path('boards/card/', views.card_create, name='card'),
    path('boards/card/<int:pk>/', views.card_detail, name='card-detail'),
    path("boards/list/", views.list_create, name="lists"),
    path('boards/list/<int:pk>/', views.list_detail, name='list-detail'),
]
