from django.test import TestCase
import unittest

# from mixer.backend.django import mixer

from rest_framework import serializers

from .serializers import BoardSerializer, ListSerializer, CardSerializer
from .models import Board, List, Card



"""
BoardSerializer
CardSerializer:
    serializer = CardSerializer(data={})
    serializer.is_valid(): ==> True / False
    serializer.save(): <=== Card instance from the db
ListSerializer:
AttachmentSerializer
"""


"""
TDD Approach:
------------
1. Write tests for the functionality you want to implement
2. Run the tests, see them fail
3. Write / implement code for the functionality
4. Run tests to make sure they're passing
"""


class BoardSerializerTest(TestCase):
    def setUp(self):
        self.board_data = {
            "name": "Test Board Name",
            "description": "Some board created during testing"
        }

    def test_is_valid(self):
        serializer = BoardSerializer(data=self.board_data)
        self.assertTrue(serializer.is_valid())

        board = serializer.save()  

        db_board = Board.objects.first()

        self.assertEqual(board, db_board)

        for field, value in self.board_data.items():
            self.assertEqual(value, getattr(db_board, field))
        
        # test for the date field 
        self.assertTrue("date", hasattr(db_board, "date"))
        self.assertIsNotNone(db_board.date)


    def test_invalid(self):
        # missing name field 
        del self.board_data["name"]
        serializer = BoardSerializer(data=self.board_data)

        self.assertFalse(serializer.is_valid())

class ListSerializerTest(TestCase):
    def setUp(self):
        self.list_data = {
            "title" : "Some title of a list created during testing"

        }
    
    def test_is_valid(self):
        serializer = ListSerializer(data=self.list_data)
        self.assertTrue(serializer.is_valid())
        list = serializer.save()

        db_list = List.objects.first()

        self.assertEqual(list, db_list)

        for field, value in self.list_data.items():
            self.assertEqual(value, getattr(db_list, field))

        # test for the created_at field 

        self.assertTrue("created_at", hasattr(db_list, "created_at"))
        self.assertIsNotNone(db_list.created_at)

    def test_invalid(self):
        del self.list_data["title"]
        serializer = ListSerializer(data=self.list_data)

        self.assertFalse(serializer.is_valid())

class CardSerializerTest(TestCase):
    def setUp(self):
        self.card_data = {
            "name": "Test Board Name",
            "description": "Some board created during testing"
        }

    def test_is_valid(self):
        serializer = CardSerializer(data=self.board_data)
        self.assertTrue(serializer.is_valid())

        card = serializer.save()  

        db_card = Card.objects.first()

        self.assertEqual(card, db_card)

        for field, value in self.card_data.items():
            self.assertEqual(value, getattr(db_card, field))
        
        # test for the date field 
        self.assertTrue("date", hasattr(db_card, "date"))
        self.assertIsNotNone(db_card.date)


    def test_invalid(self):
        # missing name field 
        del self.card_data["name"]
        serializer = CardSerializer(data=self.card_data)

        self.assertFalse(serializer.is_valid())


class AttachmentsSerializerTest(TestCase):
    def 


# class TestList:
#     def test_str(self):
#         list = mixer.blend('boards.List')
#         assert list.title == str(list), 'Should check the List name'

#     def test_save(self):
#         board = mixer.blend('boards.Board')
#         list1 = mixer.blend('boards.List', board=board)
#         list2 = mixer.blend('boards.List', board=board)
#         assert list1.order == 2 ** 16 - 1 
#         assert list1.order == list2.order - (2 ** 16 - 1)
#         list3 = mixer.blend('boards.List', board=board)
#         list4 = mixer.blend('boards.List', board=board)
#         list1.delete()
#         list5 = mixer.blend('boards.List', board=board)
#         assert list5.order == 5 * (2 ** 16 - 1)