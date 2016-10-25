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

from test.db import BaseDatabaseTest

from dino.config import UserKeys

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'


class DatabaseRedisTest(BaseDatabaseTest):
    def setUp(self):
        self.set_up_env('redis')

    def tearDown(self):
        self.db.redis.flushall()
        self.env.cache._flushall()

    def test_is_admin_before_create(self):
        self._test_is_admin_before_create()

    def test_is_admin_after_create(self):
        self._test_is_admin_after_create()

    def test_is_admin_after_create_set_admin(self):
        self._test_is_admin_after_create_set_admin()

    def test_channel_for_room_no_channel(self):
        self._test_channel_for_room_no_channel()

    def test_channel_for_room_with_channel_without_room(self):
        self._test_channel_for_room_with_channel_without_room()

    def test_channel_for_room_with_channel_with_room(self):
        self._test_channel_for_room_with_channel_with_room()

    def test_leave_room_not_joined(self):
        self._test_leave_room_not_joined()

    def test_leave_room_joined(self):
        self._test_leave_room_joined()

    def test_set_moderator_no_room(self):
        self._test_set_moderator_no_room()

    def test_set_moderator_with_room(self):
        self._test_set_moderator_with_room()

    def test_set_room_owner_no_room(self):
        self._test_set_room_owner_no_room()

    def test_set_room_owner_with_room(self):
        self._test_set_room_owner_with_room()

    def test_set_channel_owner_no_channel(self):
        self._test_set_channel_owner_no_channel()

    def test_set_channel_owner_with_channel(self):
        self._test_set_channel_owner_with_channel()

    def test_get_user_status_before_set(self):
        self._test_get_user_status_before_set(UserKeys.STATUS_UNAVAILABLE)

    def test_set_user_offline(self):
        self._test_set_user_offline(UserKeys.STATUS_UNAVAILABLE)

    def test_set_user_online(self):
        self._test_set_user_online(UserKeys.STATUS_AVAILABLE)

    def test_set_user_invisible(self):
        self._test_set_user_invisible(UserKeys.STATUS_INVISIBLE)

    def test_remove_current_rooms_for_user_before_joining(self):
        self._test_remove_current_rooms_for_user_before_joining()

    def test_remove_current_rooms_for_user_after_joining(self):
        self._test_remove_current_rooms_for_user_after_joining()

    def test_rooms_for_user_before_joining(self):
        self._test_rooms_for_user_before_joining()

    def test_create_existing_room_name(self):
        self._test_create_existing_room_name()

    def test_rooms_for_user_after_joining(self):
        self._test_rooms_for_user_after_joining()

    def test_rooms_for_channel_before_create_channel(self):
        self._test_rooms_for_channel_before_create_channel()

    def test_rooms_for_channel_after_create_channel_before_create_room(self):
        self._test_rooms_for_channel_after_create_channel_before_create_room()

    def test_rooms_for_channel_after_create_channel_after_create_room(self):
        self._test_rooms_for_channel_after_create_channel_after_create_room()

    def test_get_channels_before_create(self):
        self._test_get_channels_before_create()

    def test_get_channels_after_create(self):
        self._test_get_channels_after_create()

    def test_room_exists(self):
        self._test_room_exists()

    def test_create_room_no_channel(self):
        self._test_create_room_no_channel()

    def test_create_existing_channel(self):
        self._test_create_existing_channel()

    def test_create_channel(self):
        self._test_create_channel()
        channels = self.db.get_channels()
        self.assertEqual(1, len(channels))

    def test_create_channel_again_to_make_sure_tables_cleared_after_each_test(self):
        self._test_create_channel()
        channels = self.db.get_channels()
        self.assertEqual(1, len(channels))

    def test_create_room(self):
        self._test_create_room()
        rooms = self.db.rooms_for_channel(BaseDatabaseTest.CHANNEL_ID)
        self.assertEqual(1, len(rooms))

    def test_create_existing_room(self):
        self._test_create_existing_room()

    def test_channel_exists_after_create(self):
        self._test_channel_exists_after_create()

    def test_channel_exists_before_create(self):
        self._test_channel_exists_before_create()

    def test_room_name_exists_before_create(self):
        self._test_room_name_exists_before_create()

    def test_room_name_exists_after_create(self):
        self._test_room_name_exists_after_create()

    def test_delete_one_non_existing_acl(self):
        self._test_delete_one_non_existing_acl()

    def test_add_one_extra_acl(self):
        self._test_add_one_extra_acl()

    def test_get_acl(self):
        self._test_get_acl()

    def test_set_acl(self):
        self._test_set_acl()

    def test_delete_one_acl(self):
        self._test_delete_one_acl()

    def test_set_room_allows_cross_group_messaging(self):
        self._test_set_room_allows_cross_group_messaging()

    def test_get_room_allows_cross_group_messaging_no_room(self):
        self._test_get_room_allows_cross_group_messaging_no_room()

    def test_get_room_allows_cross_group_messaging(self):
        self._test_get_room_allows_cross_group_messaging()

    def test_get_room_does_not_allow_cross_group_messaging(self):
        self._test_get_room_does_not_allow_cross_group_messaging()

    def test_room_allows_cross_group_messaging_no_room(self):
        self._test_room_allows_cross_group_messaging_no_room()

    def test_room_allows_cross_group_messaging(self):
        self._test_room_allows_cross_group_messaging()

    def test_room_does_not_allow_cross_group_messaging_no_room(self):
        self._test_room_does_not_allow_cross_group_messaging_no_room()
