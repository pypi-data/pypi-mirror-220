import unittest

import os
import jwt
import datetime
import requests_mock
from collections import namedtuple
from hashlib import md5

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

os.environ['PRIVATE_KEY'] = open('private.pem').read()
from dgp_oauth2 import models, controllers, credentials

class UserAdminTest(unittest.TestCase):

    USERID = 'uusseerriidd'
    NAME = 'nnaammee'
    EMAIL = 'eemmaaiill'
    AVATAR_URL = 'aavvaattaarr__uurrll'
    USERNAME = 'Usernaaaame'

    # Actions

    def setUp(self):
        self.models = models.Models()
        self.ctrl = controllers.Controllers(self.models)
        self.private_key = credentials.private_key
        self.private_token = credentials.private_token

    def test___create_user___success(self):
        user = self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        hash_of_email = md5(self.EMAIL.encode('utf8')).hexdigest()
        self.assertEqual(user['id'], hash_of_email)
        self.assertEqual(user['name'], self.NAME)
        self.assertEqual(user['email'], self.EMAIL)
        self.assertEqual(user['avatar_url'], self.AVATAR_URL)
        self.assertEqual(user['username'], self.USERNAME.lower())

    def test___update_user___success(self):
        self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        self.models.create_or_get_user(self.USERID+'2', self.NAME+'2', self.USERNAME+'2', self.EMAIL, self.AVATAR_URL+'2')
        hash_of_email = md5(self.EMAIL.encode('utf8')).hexdigest()
        user = self.models.get_user(hash_of_email)
        self.assertEqual(user['id'], hash_of_email)
        self.assertEqual(user['provider_id'], self.USERID+'2')
        self.assertEqual(user['name'], self.NAME+'2')
        self.assertEqual(user['email'], self.EMAIL)
        self.assertEqual(user['avatar_url'], self.AVATAR_URL+'2')
        self.assertEqual(user['username'], self.USERNAME.lower()+'2')

    def test___delete_user___success(self):
        self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        hash_of_email = md5(self.EMAIL.encode('utf8')).hexdigest()
        user = self.models.get_user(hash_of_email)
        self.assertEqual(user['email'], self.EMAIL)
        self.models.delete_user(hash_of_email)
        user = self.models.get_user(hash_of_email)
        self.assertIsNone(user)
        
    def test___create__existing_user___success(self):
        self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        user = self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        hash_of_email = md5(self.EMAIL.encode('utf8')).hexdigest()
        self.assertEqual(user['id'], hash_of_email)
        self.assertEqual(user['name'], self.NAME)
        self.assertEqual(user['email'], self.EMAIL)
        self.assertEqual(user['avatar_url'], self.AVATAR_URL)

    def test___get__existing_user___success(self):
        self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        hash = self.models.hash_email(self.EMAIL)
        user = self.models.get_user(hash)
        hash_of_email = md5(self.EMAIL.encode('utf8')).hexdigest()
        self.assertEqual(user['id'], hash_of_email)
        self.assertEqual(user['name'], self.NAME)
        self.assertEqual(user['email'], self.EMAIL)
        self.assertEqual(user['avatar_url'], self.AVATAR_URL)

    def test___get__nonexisting_user___success(self):
        hash = self.models.hash_email('random@mail.com')
        user = self.models.get_user(hash)
        self.assertIs(user, None)

    def test___update___no_jwt(self):
        ret = self.ctrl.update(None, 'new_username', self.private_token)
        self.assertFalse(ret.get('success'))
        self.assertEqual(ret.get('error'), 'No token')

    def test___update___bad_jwt(self):
        ret = self.ctrl.update('bla', 'new_username', self.private_token)
        self.assertFalse(ret.get('success'))
        self.assertEqual(ret.get('error'), 'Not authenticated')

    def test___update___no_such_user(self):
        hash = self.models.hash_email(self.EMAIL+'X')
        token = {
            'userid': hash,
            'exp': (datetime.datetime.utcnow() +
                    datetime.timedelta(days=14))
        }
        client_token = jwt.encode(token, self.private_token)
        ret = self.ctrl.update(client_token, 'new_username', self.private_token)
        self.assertFalse(ret.get('success'))
        self.assertEqual(ret.get('error'), 'Unknown User')

    def test___update___new_user(self):
        self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        hash = self.models.hash_email(self.EMAIL)
        token = {
            'userid': hash,
            'exp': (datetime.datetime.utcnow() +
                    datetime.timedelta(days=14))
        }
        client_token = jwt.encode(token, self.private_token)
        ret = self.ctrl.update(client_token, 'new_username', self.private_token)
        self.assertFalse(ret.get('success'))
        self.assertEqual(ret.get('error'), 'Cannot modify username, already set')

    def test___get__user_by_username___success(self):
        self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        # Get user by uppercased username
        ret = self.models.get_user_by_username(self.USERNAME.upper())
        self.assertEqual(ret.get('username'), self.USERNAME.lower())

    def test___get__users___success(self):
        self.models.create_or_get_user(self.USERID, self.NAME, self.USERNAME, self.EMAIL, self.AVATAR_URL)
        # Get user by uppercased username
        ret = self.models.get_users()
        self.assertEqual(ret[0].get('username'), self.USERNAME.lower())


class AuthenticationTest(unittest.TestCase):

    USERID = 'userid'
    IDHASH = md5(USERID.encode('utf8')).hexdigest()

    # Actions

    def setUp(self):

        self.models = models.Models()
        self.ctrl = controllers.Controllers(self.models)
        self.private_key = credentials.private_key
        self.private_token = credentials.private_token

        # Cleanup
        self.addCleanup(patch.stopall)

        self.goog_provider = namedtuple("resp",['headers'])({'Location':'google'})
        self.oauth_response = {
            'access_token': 'access_token'
        }
        goog = namedtuple('_google_remote_app',
                          ['authorize', 'authorized_response', 'name'])(
            lambda **kwargs: self.goog_provider,
            lambda **kwargs: self.oauth_response,
            'google'
        )
        self.ctrl.remote_apps['google'] = {
            'app': goog,
            'get_profile': 'https://www.googleapis.com/oauth2/v1/userinfo',
            'auth_header_prefix': 'OAuth '
        }
        self.models.get_user = Mock(
            return_value=namedtuple('User',
                                    ['name','email','avatar_url'])
            ('moshe','email@moshe.com','http://google.com')
        )
        self.ctrl._get_user_profile = Mock(
            return_value={
                'id': 'userid',
                'idhash': self.IDHASH,
                'name': 'Moshe',
                'email': 'email@moshe.com',
                'picture': 'http://moshe.com/picture'
            }
        )

    # Tests

    def test___check___no_jwt(self):
        ret = self.ctrl.authenticate(None, 'next', 'callback', self.private_token)
        self.assertFalse(ret.get('authenticated'))
        self.assertIsNotNone(ret.get('providers',{}).get('google'))

    def test___check___bad_jwt(self):
        ret = self.ctrl.authenticate('bla', 'next', 'callback', self.private_token)
        self.assertFalse(ret.get('authenticated'))
        self.assertIsNotNone(ret.get('providers',{}).get('google'))

    def test___check___good_jwt_no_such_user(self):
        self.models.get_user = Mock(
            return_value=None
        )
        token = {
            'userid': self.IDHASH,
            'exp': (datetime.datetime.utcnow() +
                    datetime.timedelta(days=14))
        }
        client_token = jwt.encode(token, self.private_token)
        ret = self.ctrl.authenticate(client_token, 'next', 'callback', self.private_token)
        self.assertFalse(ret.get('authenticated'))
        self.assertIsNotNone(ret.get('providers',{}).get('google'))

    def test___check___expired_jwt(self):
        token = {
            'userid': self.IDHASH,
            'exp': (datetime.datetime.utcnow() -
                    datetime.timedelta(days=1))
        }
        client_token = jwt.encode(token, self.private_token)
        ret = self.ctrl.authenticate(client_token, 'next', 'callback', self.private_token)
        self.assertFalse(ret.get('authenticated'))
        self.assertIsNotNone(ret.get('providers',{}).get('google'))

    def test___check___good_jwt(self):
        token = {
            'userid': self.IDHASH,
            'exp': (datetime.datetime.utcnow() +
                    datetime.timedelta(days=14))
        }
        client_token = jwt.encode(token, self.private_token)
        ret = self.ctrl.authenticate(client_token, 'next', 'callback', self.private_token)
        self.assertTrue(ret.get('authenticated'))
        self.assertIsNotNone(ret.get('profile'))
        self.assertEqual(ret['profile'].email,'email@moshe.com')
        self.assertEqual(ret['profile'].avatar_url,'http://google.com')
        self.assertEqual(ret['profile'].name,'moshe')

    def test___callback___good_response(self):
        token = {
            'next': 'http://next.com/',
            'provider': 'google',
            'exp': (datetime.datetime.utcnow() +
                    datetime.timedelta(days=14))
        }
        state = jwt.encode(token, self.private_token)
        ret = self.ctrl.oauth_callback(state, 'callback', self.private_token)
        self.assertTrue('jwt' in ret)

    def test___callback___good_response_double(self):
        token = {
            'next': 'http://next.com/',
            'provider': 'google',
            'exp': (datetime.datetime.utcnow() +
                    datetime.timedelta(days=14))
        }
        state = jwt.encode(token, self.private_token)
        ret = self.ctrl.oauth_callback(state, 'callback', self.private_token)
        self.assertTrue('jwt' in ret)
        ret = self.ctrl.oauth_callback(state, 'callback', self.private_token)
        self.assertTrue('jwt' in ret)

    def test___callback___bad_response(self):
        self.oauth_response = None
        token = {
            'next': 'http://next.com/',
            'provider': 'google',
            'exp': (datetime.datetime.utcnow() +
                    datetime.timedelta(days=14))
        }
        state = jwt.encode(token, self.private_token)
        ret = self.ctrl.oauth_callback(state, 'callback', self.private_token)
        self.assertFalse('jwt' in ret)

    def test___callback___bad_state(self):
        ret = self.ctrl.oauth_callback("das", 'callback', self.private_token)
        self.assertFalse('jwt' in ret)


class GetUserProfileTest(unittest.TestCase):

    def setUp(self):

        self.models = models.Models()
        self.ctrl = controllers.Controllers(self.models)
        self.private_key = credentials.private_key
        self.private_token = credentials.private_token

        # Cleanup
        self.addCleanup(patch.stopall)

        self.goog_provider = namedtuple("resp",['headers'])({'Location':'google'})
        self.git_provider = namedtuple("resp",['headers'])({'Location':'github'})
        self.oauth_response = {
            'access_token': 'access_token'
        }
        goog = namedtuple('_google_remote_app',
                          ['authorize', 'authorized_response', 'name'])(
            lambda **kwargs: self.goog_provider,
            lambda **kwargs: self.oauth_response,
            'google'
        )
        git = namedtuple('_github_remote_app',
                        ['authorize', 'authorized_response', 'name'])(
            lambda **kwargs: self.git_provider,
            lambda **kwargs: self.oauth_response,
            'github'
        )
        self.ctrl.remote_apps['google'] = {
            'app': goog,
            'get_profile': 'https://www.googleapis.com/oauth2/v1/userinfo',
            'auth_header_prefix': 'OAuth '
        }
        self.ctrl.remote_apps['github'] = {
            'app': git,
            'get_profile': 'https://api.github.com/user',
            'auth_header_prefix': 'OAuth '
        }
        self.mocked_resp = '''
        {
            "name": "Moshe",
            "email": "email@moshe.com"
        }
        '''

    # Tests

    def test___check___getting_none_if_no_token(self):
        res = self.ctrl._get_user_profile('google', None)
        self.assertIsNone(res)

    def test___check___google_works_fine(self):
        with requests_mock.Mocker() as mock:
            mock.get('https://www.googleapis.com/oauth2/v1/userinfo',
                    text=self.mocked_resp)
            res = self.ctrl._get_user_profile('google', 'access_token')
            self.assertEqual(res['email'], 'email@moshe.com')
            self.assertEqual(res['name'], 'Moshe')


    def test___check___git_works_fine_with_public_email(self):
        with requests_mock.Mocker() as mock:
            emails_resp = '''
            [{
                "email": "email@moshe.com",
                "primary": true,
                "verified": true
             }]
            '''
            mock.get('https://api.github.com/user', text=self.mocked_resp)
            mock.get('https://api.github.com/user/emails', text=emails_resp)
            res = self.ctrl._get_user_profile('github', 'access_token')
            self.assertEqual(res['email'], 'email@moshe.com')
            self.assertEqual(res['name'], 'Moshe')


    def test___check___git_works_fine_with_private_email(self):
        self.mocked_resp = '''
        {
            "name": "Moshe",
            "email": null
        }
        '''
        emails_resp = '''
        [{
            "email": "email@moshe.com",
            "primary": true,
            "verified": true
         }]
        '''
        with requests_mock.Mocker() as mock:
            mock.get('https://api.github.com/user', text=self.mocked_resp)
            mock.get('https://api.github.com/user/emails', text=emails_resp)
            res = self.ctrl._get_user_profile('github', 'access_token')
            self.assertEqual(res['email'], 'email@moshe.com')
            self.assertEqual(res['name'], 'Moshe')


    def test___check___git_works_fine_if_multiple_emails_and_one_exists(self):
        self.mocked_resp = '''
        {
            "name": "Moshe",
            "email": null
        }
        '''
        emails_resp = '''
        [{
            "email": "email@newuser.com",
            "primary": false,
            "verified": true
         },
         {
             "email": "email@another.com",
             "primary": true,
             "verified": true
          }
        ]
        '''
        with requests_mock.Mocker() as mock:
            self.models.create_or_get_user('gtihib', '', '', 'email@newuser.com', '')
            mock.get('https://api.github.com/user', text=self.mocked_resp)
            mock.get('https://api.github.com/user/emails', text=emails_resp)
            res = self.ctrl._get_user_profile('github', 'access_token')
            self.assertEqual(res['email'], 'email@newuser.com')
            self.assertEqual(res['name'], 'Moshe')


class NormalizeProfileTestCase(unittest.TestCase):

    def setUp(self):

        self.models = models.Models()
        self.ctrl = controllers.Controllers(self.models)

        # Cleanup
        self.addCleanup(patch.stopall)


    def test__normalize_profile_from_github(self):
        git_response = {
            'id': 'gituserid',
            'login': 'NotMoshe',
            'name': 'Not Moshe',
            'email': 'git_email@moshe.com'
        }
        out = self.ctrl._normalize_profile('github', git_response)
        self.assertEqual(out['username'], 'NotMoshe')

    def test__normalize_profile_from_google(self):
        google_response = {
            'id': 'userid',
            'name': 'Moshe',
            'email': 'google_email@moshe.com'
        }
        out = self.ctrl._normalize_profile('google', google_response)
        self.assertEqual(out['username'], 'google_email')

    def test__adds_number_if_username_already_exists(self):
        self.models.save_user({
            'id': 'new_userid',
            'provider_id': '',
            'username': 'existing_username',
            'name': 'Moshe',
            'email': 'email@moshe.com',
            'avatar_url': 'http://avatar.com',
            'join_date': datetime.datetime.now()
        })
        google_response = {
            'id': 'userid',
            'username': 'existing_username',
            'name': 'Moshe',
            'email': 'existing_username@moshe.com'
        }
        out = self.ctrl._normalize_profile('google', google_response)
        self.assertEqual(out['username'], 'existing_username1')


class ResolveUsernameTest(unittest.TestCase):

    def setUp(self):

        self.models = models.Models()
        self.ctrl = controllers.Controllers(self.models)
        self.private_key = credentials.private_key
        self.private_token = credentials.private_token

        # Cleanup
        self.addCleanup(patch.stopall)

    def test___resolve_username___existing_user(self):
        self.models.get_user_by_username = Mock(
            return_value={'id': 'abc123'}
        )
        username = 'existing_user'
        ret = self.ctrl.resolve_username(username)
        self.assertEqual(ret['userid'], 'abc123')

    def test___resolve_username___nonexisting_user(self):
        username = 'nonexisting_user'
        ret = self.ctrl.resolve_username(username)
        self.assertEqual(ret['userid'], None)


class GetUserProfileByUsernameTest(unittest.TestCase):

    def setUp(self):

        self.models = models.Models()
        self.ctrl = controllers.Controllers(self.models)
        self.private_key = credentials.private_key
        self.private_token = credentials.private_token

        # Cleanup
        self.addCleanup(patch.stopall)

    def test___get_profile_by_username___existing_user(self):
        return_value = {
            'id': 'abc123',
            'email': 'test@test.com',
            'join_date': 'Mon, 24 Jul 2017 12:17:50 GMT',
            'name': 'Test Test',
            'avatar_url': 'https://avatar.com'
        }
        self.models.get_user_by_username = Mock(
            return_value=return_value
        )

        username = 'existing_user'
        ret = self.ctrl.get_profile_by_username(username)
        self.assertEqual(ret['profile']['id'], return_value['id'])
        self.assertEqual(ret['profile']['name'], return_value['name'])
        self.assertEqual(ret['profile']['join_date'], return_value['join_date'])
        self.assertEqual(ret['profile']['avatar_url'], return_value['avatar_url'])
        self.assertEqual(ret['profile']['gravatar'], self.models.hash_email(return_value['email']))
        self.assertEqual(ret['found'], True)

    def test___get_profile_by_username___nonexisting_user(self):
        username = 'nonexisting_user'
        ret = self.ctrl.get_profile_by_username(username)
        self.assertEqual(ret['profile'], None)
        self.assertEqual(ret['found'], False)


class FakeAuthenticationTest(unittest.TestCase):

    # Actions

    def setUp(self):

        self.models = models.Models()
        self.ctrl = controllers.Controllers(self.models)
        self.private_key = credentials.private_key
        self.private_token = credentials.private_token

    # Tests

    def test___check___flow(self):
        ret = self.ctrl.authenticate(None, 'next', 'callback', self.private_token)
        self.assertFalse(ret.get('authenticated'))
        self.assertIsNotNone(ret.get('providers',{}).get('google'))
        self.assertIsNotNone(ret.get('providers',{}).get('github'))

        url = ret['providers']['google']['url']
        token = url.split('jwt=')[1]
        self.assertIsNotNone(token)
        self.assertNotEqual(token, '')

        user = self.models.get_user(self.models.FAKE_USER_ID)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], self.models.FAKE_USER_RECORD['email'])

        users = self.models.get_users()
        self.assertIsNotNone(users)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['email'], self.models.FAKE_USER_RECORD['email'])

        ret = self.ctrl.authenticate(token, 'next', 'callback', self.private_token)
        self.assertTrue(ret.get('authenticated'))
        self.assertIsNotNone(ret.get('profile'))
        self.assertEqual(ret['profile']['email'], self.models.FAKE_USER_RECORD['email'])
        self.assertEqual(ret['profile']['avatar_url'], self.models.FAKE_USER_RECORD['avatar_url'])
        self.assertEqual(ret['profile']['name'], self.models.FAKE_USER_RECORD['name'])
