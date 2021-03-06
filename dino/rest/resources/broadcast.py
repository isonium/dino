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

from dino import environ
from dino import utils
from dino.utils.decorators import timeit
from dino.db.manager import UserManager
from dino.rest.resources.base import BaseResource

from flask import request

logger = logging.getLogger(__name__)

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'


def fail(error_message):
    return {
        'status': 'FAIL',
        'message': error_message
    }


class BroadcastResource(BaseResource):
    def __init__(self):
        super(BroadcastResource, self).__init__()
        self.user_manager = UserManager(environ.env)
        self.request = request

    @timeit(logger, 'on_rest_broadcast')
    def do_post(self):
        is_valid, msg, json = self.validate_json(self.request, silent=False)
        if not is_valid:
            logger.error('invalid json: %s' % msg)
            raise RuntimeError('invalid json')

        if json is None:
            raise RuntimeError('no json in request')
        if not isinstance(json, dict):
            raise RuntimeError('need a dict')

        logger.debug('POST request: %s' % str(json))

        if 'body' not in json:
            raise RuntimeError('no key [body] in json message')
        if 'verb' not in json:
            raise RuntimeError('no key [verb] in json message')

        body = json.get('body')
        if body is None or len(body.strip()) == 0:
            raise RuntimeError('body may not be blank')
        if not utils.is_base64(body):
            raise RuntimeError('body in json message must be base64')

        verb = json.get('verb')
        if verb is None or len(verb.strip()) == 0:
            raise RuntimeError('verb may not be blank')

        data = utils.activity_for_broadcast(body, verb)
        environ.env.out_of_scope_emit('gn_broadcast', data, json=True, namespace='/ws', broadcast=True)
