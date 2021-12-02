from django.db.models import fields
from rest_framework import serializers 

from .models import Board, List


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        exclude = ['board']

    # def get_items(self, obj):
    #     queryset = Item.objects.filter(list=obj).order_by('order')
    #     return ItemSerializer(queryset, many=True).data