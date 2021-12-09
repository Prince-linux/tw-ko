from django.db.models import fields
from rest_framework import serializers 

from .models import Board, Card, List, Attachment


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"



class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = "__all__"


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ("attachments",)

class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = '__all__'