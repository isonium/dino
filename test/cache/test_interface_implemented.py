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

import unittest
from nose_parameterized import parameterized

from dino.cache import ICache
from dino.cache.redis import CacheRedis

__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'


class RedisHasInterfaceMethodsTest(unittest.TestCase):
    interface_methods = [name for name in ICache.__dict__['_InterfaceClass__attrs'].keys()]

    def setUp(self):
        self.redis_methods = set(
                [
                    key for key in CacheRedis.__dict__.keys()
                    if not key.startswith('_') and callable(CacheRedis.__dict__[key])
                ]
        )

    @parameterized.expand(interface_methods)
    def test_method_is_implemented(self, method):
        self.assertIn(method, self.redis_methods)


class RedisHasOnlyInterfaceMethodsTest(unittest.TestCase):
    redis_methods = set(
            [
                key for key in CacheRedis.__dict__.keys()
                if not key.startswith('_') and callable(CacheRedis.__dict__[key])
            ]
    )

    def setUp(self):
        self.interface_methods = [name for name in ICache.__dict__['_InterfaceClass__attrs'].keys()]

    @parameterized.expand(redis_methods)
    def test_method_is_in_interface(self, method):
        self.assertIn(method, self.interface_methods)
