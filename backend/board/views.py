from django.shortcuts import render

# Create your views here.


from rest_framework import serializers, viewsets

from board.models import Board, Card, List,  Attachment

from .serializers import BoardSerializer, CardSerializer, ListSerializer, AttachmentSerializer


class BoardView(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()