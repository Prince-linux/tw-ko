from django.shortcuts import render

# Create your views here.


# from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework import status 
from rest_framework.response import Response 

from board.models import Board, Card, List,  Attachment

from .serializers import BoardSerializer, CardSerializer, ListSerializer, AttachmentSerializer

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

  
@api_view(['GET','PUT','DELETE'])
def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    if request.method == 'GET':
        serializer = BoardSerializer(board)
        return Response(serializer.data)
  
    elif request.method == 'PUT':
        serializer = BoardSerializer(board, data=request.data)
  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    elif request.method == 'DELETE':
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def card_create(request):
    """
    Gets a list of boards if request.method is GET 
    or creates an attachment if request.method is POST
    :param request:
    :returns:
    """
    if request.method == "POST":
        serializer = CardSerializer(data=request.data)
        if not serializer.is_valid():
            """
            data = {
                success: True / False,a
                errors: errors that occured.
            }
            """
            return Response(data={"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(data={"success": True, "board": serializer.data}, status=status.HTTP_201_CREATED)


    card = Card.objects.all()

    serializer = CardSerializer(card, many=True)

    return Response(data={"success": True, "boards": serializer.data})



@api_view(['GET', 'PUT', 'DELETE'])
def list_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
        list = List.objects.get(pk=pk)
    except Board.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    if request.method == 'GET':
        list = List.objects.get(pk=pk)
        serializer = ListSerializer(list, board)
        return Response(serializer.data)
  
    elif request.method == 'PUT':
        serializer = ListSerializer(list, data=request.data)
  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    elif request.method == 'DELETE':
        list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def attachment_create(request):
    """
    Gets a list of boards if request.method is GET 
    or creates an attachment if request.method is POST
    :param request:
    :returns:
    """
    if request.method == "POST":
        serializer = AttachmentSerializer(data=request.data)
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


    attachment = Attachment.objects.all()

    serializer = AttachmentSerializer(attachment, many=True)

    return Response(data={"success": True, "boards": serializer.data})


@api_view(['GET', 'DELETE'])
def attachment_detail(request, pk):
    try:
        attachment = Attachment.objects.get(pk=pk)
    except Attachment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    if request.method == 'GET':
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data)
  
    elif request.method == 'DELETE':
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)











































# @api_view(['GET','PUT','PATCH','DELETE'])
# def board_detail(request, pk):
#     try:
#         board = Board.objects.get(pk=pk)
#     except Board.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
  
#     if request.method == 'GET':
#         serializer = BoardSerializer(board)
#         return Response(serializer.data)
  
#     elif request.method == 'PUT':
#         serializer = BoardSerializer(board, data=request.data)
  
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'PATCH':
#         serializer = BoardSerializer(board, data=request.data, partial=True)
  
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)
  
#     elif request.method == 'DELETE':
#         board.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

