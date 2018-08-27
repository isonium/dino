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

from dino.db.manager.channels import ChannelManager
from dino.db.manager.rooms import RoomManager
from dino.db.manager.users import UserManager
from dino.db.manager.acls import AclManager
from dino.db.manager.storage import StorageManager
from dino.db.manager.blacklist import BlackListManager
from dino.db.manager.broadcast import BroadcastManager
from dino.db.manager.spam import SpamManager

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'
