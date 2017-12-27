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

from dino import environ
from dino import utils
from dino.utils.decorators import timeit
from dino.rest.resources.base import BaseResource

from flask import request

logger = logging.getLogger(__name__)

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'


class BlacklistResource(BaseResource):
    def __init__(self):
        super(BlacklistResource, self).__init__()
        self.request = request

    def decode_or_throw(self, b64_word: str) -> str:
        if not utils.is_base64(b64_word):
            logger.error('word is not base64 encoded: "%s"' % b64_word)
            raise RuntimeError('word is not base64 encoded: "%s"' % b64_word)

        try:
            return utils.b64d(b64_word)
        except Exception as e:
            logger.error('could not decode base64 word "%s": %s' % (str(b64_word), str(e)))
            raise RuntimeError('could not decode base64 word "%s": %s' % (str(b64_word), str(e)))

    def validate_and_get_word(self):
        is_valid, msg, json = self.validate_json()
        if not is_valid:
            logger.error('invalid json: %s' % msg)
            raise RuntimeError('invalid json')

        if json is None:
            raise RuntimeError('no json in request')
        if not isinstance(json, dict):
            raise RuntimeError('need a dict')

        if 'word' not in json:
            raise RuntimeError('no word parameter in request')

        return json

    @timeit(logger, 'on_rest_blacklist_add')
    def do_post(self):
        json = self.validate_and_get_word()
        logger.debug('POST request: %s' % str(json))
        word = self.decode_or_throw(json.get('word'))

        try:
            environ.env.db.add_words_to_blacklist([word])
        except Exception as e:
            logger.error('could not add word "%s" to blacklist: %s' % (str(word), str(e)))
            logger.exception(traceback.format_exc())
            raise RuntimeError('could not add word "%s" to blacklist: %s' % (str(word), str(e)))

    @timeit(logger, 'on_rest_blacklist_delete')
    def do_delete(self):
        json = self.validate_and_get_word()
        logger.debug('DELETE request: %s' % str(json))
        word = self.decode_or_throw(json.get('word'))

        try:
            environ.env.db.remove_matching_word_from_blacklist(word)
        except Exception as e:
            logger.error('could not remove word "%s" from blacklist: %s' % (str(word), str(e)))
            logger.exception(traceback.format_exc())
            raise RuntimeError('could not remove word "%s" from blacklist: %s' % (str(word), str(e)))

    def validate_json(self):
        try:
            return True, None, self.request.get_json(silent=False)
        except Exception as e:
            logger.error('error: %s' % str(e))
            logger.exception(traceback.format_exc())
            return False, 'invalid json in request', None
