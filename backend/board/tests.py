from django.test import TestCase
from django.urls import reverse 
import unittest

# from mixer.backend.django import mixer
from rest_framework.test import APITestCase, APIClient

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
        # board_author = User.objects.create(username="tester")
        board = Board.objects.create(name="Test Name", description="Some testing board")
        self.list_data = {
            "title" : "Some title of a list created during testing",
            "board": board.pk
        }
    
    def test_is_valid(self):
        serializer = ListSerializer(data=self.list_data)
        self.assertTrue(serializer.is_valid())
        list = serializer.save()

        db_list = List.objects.first()

        self.assertEqual(list, db_list)

        self.assertEqual(db_list.title, self.list_data["title"])
        self.assertEqual(db_list.board.pk, self.list_data["board"])

        # test for the created_at field 

        self.assertTrue("created_at", hasattr(db_list, "created_at"))
        self.assertIsNotNone(db_list.created_at)

    def test_invalid(self):
        del self.list_data["title"]
        serializer = ListSerializer(data=self.list_data)

        self.assertFalse(serializer.is_valid())

class CardSerializerTest(TestCase):
    def setUp(self):
        # create a list
        self.card_data = {
            "description": "Some board created during testing"
        }

    def test_is_valid(self):
        serializer = CardSerializer(data=self.card_data)
        self.assertTrue(serializer.is_valid())

        card = serializer.save()  

        db_card = Card.objects.first()

        self.assertEqual(card, db_card)

        for field, value in self.card_data.items():
            self.assertEqual(value, getattr(db_card, field))
        
        # test for the date field 
        self.assertTrue(hasattr(db_card, "created_at"))
        self.assertIsNotNone(db_card.created_at)


    def xtest_invalid(self):
        # missing name field 
        serializer = CardSerializer(data=self.card_data)

        self.assertFalse(serializer.is_valid())


class BoardViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_all_boards(self):
        response = self.client.get(reverse("boards"))
        
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.status_code, 200)

        response_boards = response.json()["boards"]

        for board in response_boards:
            db_board = Board.objects.get(name=board["name"])

            for key, value in board.items():
                self.assertEqual(value, getattr(db_board, key))
    
    def test_create_board(self):
        data = {
            "name": "Board name", 
            "description": "Board description"
        }
        response = self.client.post(reverse("boards"), data=data) 

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["success"])

        db_board = Board.objects.get(name=data["name"])

        self.assertEqual(data["name"], db_board.name)
        self.assertEqual(data["description"], db_board.description)

        response_board = response.json()["board"]

        self.assertEqual(data["name"], response_board["name"])
        self.assertEqual(data["description"], response_board["description"])
    
    # def test_board_detail(self):
    #     data = {
    #         "board": "
    #     }

        