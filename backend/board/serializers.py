from django.db.models import fields
from rest_framework import serializers

from .models import Board, Card, List, Attachment


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     import pdb
    #     pdb.set_trace()


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = "__all__"


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = '__all__'
