import os

from tornado import testing

from . import base


class FailoverTests(base.AsyncTestCase):

    AUTO_CONNECT = False

    def setUp(self):
        super(FailoverTests, self).setUp()
        self.reset_slave_relationship()

    @property
    def redis_port(self):
        return int(os.environ['REDIS2_PORT'])

    @testing.gen_test
    def test_that_hset_writes_to_master(self):
        yield self.client.connect()
        expectation = (self.client._connection.host,
                       self.client._connection.port)
        key, field, value = self.uuid4(3)
        result = yield self.client.hset(key, field, value)
        self.assertEqual(result, 1)
        redis_addr = (self.client._connection.host,
                      self.client._connection.port)
        self.assertNotEqual(redis_addr, expectation)
