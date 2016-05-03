from django.test import SimpleTestCase


class GithubTaskTests(SimpleTestCase):

    def test_basic_test(self):
        test = 4+1
        self.assertEqual(test, 5)
