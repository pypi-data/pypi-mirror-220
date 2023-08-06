import unittest
import jwt

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
from importlib import import_module

from dgp_oauth2.controllers import Controllers
from dgp_oauth2.models import Models
credentials = import_module('dgp_oauth2.credentials')


class ExtensionsTestCase(unittest.TestCase):

    def setUp(self):

        self.models = Models()
        self.ctrl = Controllers(self.models)
        # Cleanup
        self.addCleanup(patch.stopall)

        # Mock response from models (to make sure it's new user)
        self.models.create_or_get_user = Mock(
            return_value={'new': True, 'id': 'test'}
        )
        self.private_token = credentials.private_token

    # Tests

    def test___check___on_new_user_is_called(self):
        profile = dict(id='test', name='name', email='test@mail.com')
        token = self.ctrl._get_token_from_profile('test_provider', profile, self.private_token)
        user_profile = jwt.decode(token, self.private_token, algorithms=['HS256'])
        self.assertEqual(user_profile.get('userid'), 'new-user')
