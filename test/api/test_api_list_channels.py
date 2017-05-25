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

from activitystreams import parse as as_parser

import os
os.environ['ENVIRONMENT'] = 'test'

from dino import api
from test.base import BaseTest

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'


class ApiListChannelsTest(BaseTest):
    def test_list_channels(self):
        self.create_and_join_room()
        self.set_owner()
        act = self.activity()
        code, act = api.on_list_channels(act, as_parser(act))
        self.assertEqual(200, code)
        self.assertEqual(BaseTest.CHANNEL_ID, act['object']['attachments'][0]['id'])

    def activity(self):
        return {
            'actor': {
                'id': BaseTest.USER_ID
            },
            'verb': 'list'
        }
