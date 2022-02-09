import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

# from mixer.backend.django import mixer
from rest_framework.test import APITestCase, APIClient

from board.serializers import BoardSerializer, ListSerializer, CardSerializer
from board.models import Board, List, Card, Attachment

from PIL import Image


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
        board = Board.objects.create(
            name="Test Name", description="Some testing board")
        self.list_data = {
            "title": "Some title of a list created during testing",
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

    def test_invalid(self):
        # missing name field
        serializer = CardSerializer(data=self.card_data)

        self.assertFalse(serializer.is_valid())


class BoardViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.board_data = {
            "name": "Test Board",
            "description": "Some board description test"
        }
        # create(name="", description="")
        self.board = Board.objects.create(**self.board_data)

    def test_get_all_boards(self):
        """
        Tests that all boards can be fetched on route: /api/boards/ -- LIST (GET)
        """

        response = self.client.get(reverse("board:boards"))

        self.assertTrue(response.json()["success"])
        self.assertEqual(response.status_code, 200)

        response_boards = response.json()["boards"]
        import pdb
        pdb.set_trace()

        for board in response_boards:
            db_board = Board.objects.get(name=board["name"])

            for key, value in board.items():
                self.assertEqual(value, getattr(db_board, key))

    def test_create_board(self):
        """
        Tests for route: /api/boards/  -- POST
        """
        data = {
            "name": "Board name",
            "description": "Board description"
        }
        response = self.client.post(reverse("board:boards"), data=data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["success"])

        db_board = Board.objects.get(name=data["name"])

        self.assertEqual(data["name"], db_board.name)
        self.assertEqual(data["description"], db_board.description)

        response_board = response.json()["board"]

        self.assertEqual(data["name"], response_board["name"])
        self.assertEqual(data["description"], response_board["description"])

    def test_get_a_single_board(self):
        """
        Tests that a single board can be fetched on route: /api/boards/<int:pk>/
        """
        # Create a board [Done]
        # hit the endpoint with the board's pk on /api/boards/<int:pk>/
        # Assert the content

        response = self.client.get(
            reverse("board:board-detail", args=(self.board.pk,)))
        self.assertEqual(response.status_code, 200)

        for field, value in self.board_data.items():
            self.assertEqual(value, getattr(self.board, field))

    def test_update_a_single_board(self):
        """
        Test that a single board can be updated on route: /api/boards/<int:pk>/
        """
        update_data = {
            "name": "James"
        }
        response = self.client.put(
            reverse("board:board-detail", args=(self.board.pk,)), data=update_data)
        self.assertEqual(response.status_code, 200)
        self.board.refresh_from_db()
        self.assertEqual(update_data['name'], self.board.name)

    def test_delete_a_single_board(self):
        """
        Test that a single board can be deleted on route: /api/boards/<int:pk>/
        """

        response = self.client.delete(
            reverse("board:board-detail", args=(self.board.pk,)))
        self.assertEqual(response.status_code,  204)

        with self.assertRaises(Board.DoesNotExist):
            # Raise does not exist
            Board.objects.get(name=self.board_data["name"])


class AttachmentViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        attachment_path = os.path.join(
            settings.BASE_DIR, "board", "tests", "resources", "FJ9zqiRWQAImHie.jpeg")
        image = open(attachment_path, "rb")

        file = SimpleUploadedFile(image.name, image.read())
        self.attachment_data = {
            "file": "FJ9zqiRWQAImHie.jpeg",
            "type": 'image'
        }
        self.attachment = Attachment.objects.create(**self.attachment_data)

    def test_get_all_attachment(self):
        """
        Tests that all boards can be fetched on route: /api/boards/ -- LIST (GET)
        """
        # import pdb; pdb.set_trace()
        response = self.client.get(reverse("board:attachments"))

        self.assertTrue(response.json()["success"])
        self.assertEqual(response.status_code, 200)
        # import pdb
        # pdb.set_trace()

        response_attachments = response.json()["attachments"]

        for attachment in response_attachments:
            db_attachment = Attachment.objects.get(
                type=attachment['type'],)

            for key, value in attachment.items():
                self.assertEqual(value, getattr(db_attachment, key))

    def test_create_attachment(self):
        image = open(
            r"/Users/peedor/Desktop/git/pee/urgent/tw-ko/backend/board/tests/resources/FJ9zqiRWQAImHie.jpeg", "rb")

        file = SimpleUploadedFile(
            image.name, image.read(), content_type='multipart/form-data')
        data = {
            "file": file,
            "type": "image"

        }

        response = self.client.post(
            reverse("board:attachments"), data=data, format='multipart')
        self.assertEqual(response.status_code,
                         201)
        # import pdb
        # pdb.set_trace()
        self.assertTrue(response.json()["success"])

        db_attachment = Attachment.objects.get(
            file=data["file"], type=data["type"])

        self.assertEqual(data["type"], db_attachment.type)
        self.assertEqual(data["file"], db_attachment.file)

        response_attachment = response.json()

        self.assertEqual(data.get(type), response_attachment.get(type))
        self.assertEqual(data.get(file), response_attachment.get(file))

    def test_get_a_single_attachment(self):
        """
        Tests that a single board can be fetched on route: /api/boards/<int:pk>/
        """
        # Create a board [Done]
        # hit the endpoint with the board's pk on /api/boards/<int:pk>/
        # Assert the content

        response = self.client.get(
            reverse("board:attachment-detail", args=(self.attachment.pk,)))
        self.assertEqual(response.status_code, 200)

        for field, value in self.attachment_data.items():
            self.assertEqual(value, getattr(self.attachment, field))

    def test_delete_a_single_attachment(self):
        """
        Test that a single board can be deleted on route: /api/boards/<int:pk>/
        """

        response = self.client.delete(
            reverse("board:attachment-detail", args=(self.attachment.pk,)))
        self.assertEqual(response.status_code,  204)

        with self.assertRaises(Attachment.DoesNotExist):
            # Raise does not exist
            Attachment.objects.get(file=self.attachment_data["file"])
