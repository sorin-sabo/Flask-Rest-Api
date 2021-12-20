import json

from flask import g
from parameterized import parameterized

from apps.api.models import User, Author
from apps.api.utils import NotFound
from tests.utils.base import BaseTestCase


class TestAuthorController(BaseTestCase):

    def test_author_that_does_not_exist(self):
        """
        Test getting an author that does not exist raises 404
        """

        with self.assertRaises(NotFound):
            response = self.client.get(
                f"/api/authors/",
                content_type="application/json",
            )

            self.assertEqual(response.status_code, 404)

    def test_get_author(self):
        """
        Test getting an author works properly
        """

        # A context user is required for force-authentication; Dropped at end of test.
        user = User.query.get(100)
        g.user = user

        # Existing author linked to the user
        author = Author.query.get(100)
        author_dict = author.__dict__

        response = self.client.get(
            f"/api/authors/",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('data', data)
        response_data = data['data']

        # Test all parameters are returned properly
        for key in response_data.keys():
            if key == 'birthday':
                self.assertEqual(author_dict[key].strftime('%Y-%m-%d'), response_data[key])
            else:
                self.assertEqual(author_dict[key], response_data[key])

        g.pop('user')

    def test_create_author(self):
        """
        Test creating an author is working properly
        """

        user = User.query.get(101)
        g.user = user

        # Save author
        author_dict = dict(
            first_name='Test First Name Create',
            last_name='Test Last Name Create',
            birthday='2004-03-05',
            books=[
                {
                    "label": "Test 1",
                    "value": 1
                },
                {
                    "label": "Test 2",
                    "value": 2
                }
            ],
        )

        response = self.client.post(
            f"/api/authors/",
            content_type="application/json",
            data=json.dumps(author_dict)
        )

        # Test save was performed successfully
        self.assertEqual(response.status_code, 200)

        # Test save response is returned properly and contains new author id
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('data', data)
        response_data = data['data']
        self.assertIsNotNone(response_data)
        self.assertIsNotNone(response_data.get('id'))
        author = Author.query.filter_by(id=response_data['id']).first()
        self.assertIsNotNone(author)

        # Test author was saved properly
        existing_author_dict = author.__dict__
        keys_to_test = author_dict.keys() - ['books']

        for key in keys_to_test:
            self.assertEqual(author_dict[key], response_data[key], existing_author_dict[key])

        g.pop('user')

    @parameterized.expand([
        (None,),
        ('',),
        (json.dumps(dict(name='Test', first_name='Test FN', last_name='Test LN'))),
        (json.dumps(dict(name=1, first_name='Test FN', last_name='Test LN'))),
    ])
    def test_create_author_raises_validation_error(self, payload=None):
        """
        Test save author raises validation error
        - test with null payload;
        - test with empty payload;
        - test with missing data;
        - test with invalid data;
        """
        user = User.query.get(100)
        g.user = user

        response = self.client.post(
            f"/api/authors/",
            content_type="application/json",
            data=json.dumps(payload)
        )

        self.assertEqual(response.status_code, 400)

    def test_update_author(self):
        """
        Test updating an author is working properly
        """

        user = User.query.get(100)
        g.user = user

        # Updated details of author
        author_dict_update = dict(
            first_name='Test First Name Update',
            last_name='Test Last Name Update',
            birthday='2021-12-21',
            books=[
                {
                    "label": "Python 3 Advanced Programming",
                    "value": 1
                },
            ],
        )

        response = self.client.post(
            f"/api/authors/",
            content_type="application/json",
            data=json.dumps(author_dict_update)
        )
        g.pop('user')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        response_data = data['data']
        self.assertIsNotNone(response_data)
        self.assertIsNotNone(response_data.get('id'))
        author = Author.query.filter_by(id=response_data['id']).first()
        self.assertIsNotNone(author)

        data = json.loads(response.get_data(as_text=True))
        response_data = data['data']

        # Test all parameters were properly saved
        for key in author_dict_update.keys():
            if key == 'books':
                pass
            else:
                self.assertEqual(author_dict_update[key], response_data[key])

    def test_author_basic_list(self):
        """
        Test author basic list - working properly
        """

        # A context user is required for force-authentication; Dropped at end of test.
        user = User.query.get(100)
        g.user = user

        response = self.client.get(
            f"/api/authors/basic/list",
            content_type="application/json",
        )

        # Test author basic list is returned properly
        self.assertEqual(response.status_code, 200)

        # Test response data structure
        data = json.loads(response.get_data(as_text=True))
        response_data = data['data']
        self.assertTrue(isinstance(response_data, list))
        expected_attributes = ['label', 'value']

        for event_request in response_data:
            for expected_attribute in expected_attributes:
                self.assertIn(expected_attribute, event_request.keys())

        # Test response data
        expected_response = [{'label': 'Author Test', 'value': 100}]
        self.assertEqual(response_data, expected_response)

        g.pop('user')
