from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
    """ A test runner that does not set up databases """

    def setup_databases(self, **kwargs):
        """ Override the database creation method in parent """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown method in parent """
        pass
