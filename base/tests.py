from common_module.test import TestCase


class TestAuth(TestCase):
    def test_auth(self):
        self.client.login()
