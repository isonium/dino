#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import traceback

from typing import Union
from zope.interface import implementer

from dino import environ
from dino.config import SessionKeys
from dino.config import ConfigKeys
from dino.config import RedisKeys
from dino.auth import IAuth

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'

logger = logging.getLogger()


@implementer(IAuth)
class AuthRedis(object):
    def __init__(self, host: str, port: int = 6379, db: int = 0):
        if environ.env.config.get(ConfigKeys.TESTING, False) or host == 'mock':
            from fakeredis import FakeStrictRedis as Redis
        else:
            from redis import Redis

        self.redis = Redis(host=host, port=port, db=db)

    def get_user_info(self, user_id: str) -> dict:
        key = RedisKeys.auth_key(user_id)
        binary_stored_session = self.redis.hgetall(key)
        stored_session = dict()

        for key, val in binary_stored_session.items():
            if type(key) == bytes:
                key = str(key, 'utf-8')
            if type(val) == bytes:
                val = str(val, 'utf-8')

            if key in [SessionKeys.token.value, SessionKeys.user_name.value, SessionKeys.user_id.value]:
                continue
            stored_session[key] = val
        return stored_session

    def update_session_for_key(self, user_id: str, session_key: str, session_value: str) -> None:
        key = RedisKeys.auth_key(user_id)
        try:
            self.redis.hset(key, session_key, session_value)
        except Exception as e:
            logger.error(
                    'could not update session for user %s; key "%s", value "%s": %s',
                    user_id, session_key, session_value, str(e))
            logger.exception(traceback.format_exc(e))

    def authenticate_and_populate_session(self, user_id: str, supplied_token: str) -> (bool, Union[None, str], Union[None, dict]):
        if user_id is None or len(user_id) == 0:
            return False, 'no user_id supplied', None
        if supplied_token is None or len(supplied_token) == 0:
            return False, 'no token supplied', None

        key = RedisKeys.auth_key(user_id)
        binary_stored_session = self.redis.hgetall(key)
        stored_session = dict()

        for key, val in binary_stored_session.items():
            if type(key) == bytes:
                key = str(key, 'utf-8')
            if type(val) == bytes:
                val = str(val, 'utf-8')
            stored_session[key] = val

        if stored_session is None or len(stored_session) == 0:
            return False, 'no session found for this user id, not logged in yet', None

        stored_token = stored_session.get(SessionKeys.token.value)
        if stored_token != supplied_token:
            logger.warning('user "%s" supplied token "%s" but stored token is "%s"' %
                                       (user_id, supplied_token, stored_token))
            return False, 'invalid token "%s" supplied for user id "%s"' % (supplied_token, user_id), None

        session = dict()
        for session_key in SessionKeys:
            if not isinstance(session_key.value, str):
                continue

            session_value = stored_session.get(session_key.value)
            if session_value is None or not isinstance(session_value, str) or len(session_value) == 0:
                continue
            session[session_key.value] = session_value

        return True, None, session
