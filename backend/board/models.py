from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


NULL_KWARGS = {"blank": True, "null": True}

class Board(models.Model):
    name = models.CharField(max_length=300)
    #author
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300, **NULL_KWARGS)
    #attachments = models.FileField(blank=True, upload_to='uploads')
    #collaborators

    def __str__(self):
        return self.title

class List(models.Model):
    board = models.ForeignKey(Board, on_delete=CASCADE, related_name='lists')
    title = models.CharField(max_length=300)
    #order = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Attachment(models.Model):
    TYPE_CHOICES = (
        ("image", "image"),
        ("document", "document"),
        ("video", "video"),
    )
    file = models.FileField(upload_to='uploads')
    type = models.CharField(max_length=300, choices=TYPE_CHOICES)


class Card(models.Model):
    list = models.ForeignKey(List, on_delete=CASCADE, related_name="cards", **NULL_KWARGS)
    description = models.TextField(**NULL_KWARGS)
    attachments = models.ManyToManyField(Attachment)
    created_at = models.DateTimeField(auto_now_add=True)
    

