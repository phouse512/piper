from django.test import TestCase


class GithubTaskTests(TestCase):

    def test_basic_test(self):
        test = 4+1
        self.assertEqual(test, 5)
