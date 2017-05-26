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

from datetime import datetime
from flask_restful import Resource

import logging
import traceback

logger = logging.getLogger(__name__)

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'


class BaseResource(Resource):
    CACHE_CLEAR_INTERVAL = 2  # 2 seconds

    def get(self):
        if (datetime.utcnow() - self._get_last_cleared()).total_seconds() > BaseResource.CACHE_CLEAR_INTERVAL:
            self._get_lru_method().cache_clear()
            self._set_last_cleared(datetime.utcnow())

        try:
            return {'status_code': 200, 'data': self.do_get()}
        except Exception as e:
            logger.error('could not do get: %s' % str(e))
            logger.exception(traceback.format_exc())
            return {'status_code': 500, 'data': str(e)}

    def post(self):
        try:
            data = self.do_post()
            return_value = {'status_code': 200}
            if data is not None:
                return_value['data'] = data
            return return_value
        except Exception as e:
            logger.error('could not do get: %s' % str(e))
            logger.exception(traceback.format_exc())
            return {'status_code': 500, 'data': str(e)}

    def delete(self):
        try:
            data = self.do_delete()
            return_value = {'status_code': 200}
            if data is not None:
                return_value['data'] = data
            return return_value
        except Exception as e:
            logger.error('could not do delete: %s' % str(e))
            logger.exception(traceback.format_exc())
            return {'status_code': 500, 'data': str(e)}

    def validate_json(self, request, silent=True):
        try:
            return True, None, request.get_json(silent=silent)
        except Exception as e:
            logger.error('error: %s' % str(e))
            logger.exception(traceback.format_exc())
            return False, 'invalid json in request', None

    def do_delete(self):
        raise NotImplementedError()

    def do_post(self):
        raise NotImplementedError()

    def do_get(self):
        raise NotImplementedError()

    def _get_lru_method(self):
        raise NotImplementedError()

    def _get_last_cleared(self):
        raise NotImplementedError()

    def _set_last_cleared(self, last_cleared):
        raise NotImplementedError()
