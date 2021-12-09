from django.shortcuts import render

# Create your views here.


from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework import status 
from rest_framework.response import Response 

from board.models import Board, Card, List,  Attachment

from .serializers import BoardSerializer, CardSerializer, ListSerializer, AttachmentSerializer


class BoardView(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()


"""
  - api/boards/   GET (LIST), POST
  - api/board/<int:pk>/  GET, UPDATE, DELETE
  - /list/<int:pk>/   GET, UPDATE, DELETE
  - /card/create
  - /card/<int:pk>/   GET, UPDATE, DELETE

  # Attachment routes
  - /attachment/create/
  - /attachment/<int:pk>/  GET, DELETE

  function based views / class based views
"""


@api_view(["GET", "POST"])
def board_list_create(request):
    """
    Gets a list of boards if request.method is GET 
    or creates a board if request.method is POST
    :param request:
    :returns:
    """
    if request.method == "POST":
        serializer = BoardSerializer(data=request.data)
        if not serializer.is_valid():
            """
            data = {
                success: True / False,
                errors: errors that occured.
            }
            """
            return Response(data={"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(data={"success": True, "board": serializer.data}, status=status.HTTP_201_CREATED)


    board = Board.objects.all()

    serializer = BoardSerializer(board, many=True)

    return Response(data={"success": True, "boards": serializer.data})