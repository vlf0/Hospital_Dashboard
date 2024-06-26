from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        suite = super().build_suite(**kwargs)
        suite.addTest(self.test_loader.discover('data', pattern='dj_test_*.py'))
        suite.addTest(self.test_loader.discover('data', pattern='dj_test.py'))
        return suite
