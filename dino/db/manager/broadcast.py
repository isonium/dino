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

from dino.db.manager.base import BaseManager
from dino.environ import GNEnvironment

from dino import utils

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'

logger = logging.getLogger(__name__)


class BroadcastManager(BaseManager):
    def __init__(self, env: GNEnvironment):
        self.env = env

    def send(self, body: str, verb: str) -> None:
        data = utils.activity_for_broadcast(body, verb)
        self.env.out_of_scope_emit('gn_broadcast', data, json=True, namespace='/ws', broadcast=True)
