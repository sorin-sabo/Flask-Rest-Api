import unittest

import pytest

from app import db, create_app
from apps.api import blueprint, models


# noinspection SpellCheckingInspection
class BaseTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def neuter_jwt(self, monkeypatch):
        def no_verify():
            pass

        from apps.api.utils import oauth

        monkeypatch.setattr(oauth, 'verify_jwt_token', no_verify)

    def setUp(self):
        self.app = create_app('testing')
        self.app.register_blueprint(blueprint)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.generic_setup()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def generic_setup():
        """
        Generic setup to have:
        - 2 users to use in all unit tests;
        - an author to use in all unit tests;

        Can be used in all unit tests:
        -   author_id=100;
        -   user_id=100;
        -   user_id=101;
        """

        # Save user
        user_dict = dict(
            id=100,
            email='author@test.com',
            first_name='Test',
            last_name='User'
        )
        user = models.User(**user_dict)
        db.session.add(user)
        db.session.commit()

        user_dict = dict(
            id=101,
            email='author2@test.com',
            first_name='Test2',
            last_name='User'
        )
        user = models.User(**user_dict)
        db.session.add(user)
        db.session.commit()

        # Save author
        author_dict = dict(
            id=100,
            first_name='Author',
            last_name='Test',
            birthday='2001-01-01',
            user_id=100
        )
        author = models.Author(**author_dict)
        db.session.add(author)
        db.session.commit()
