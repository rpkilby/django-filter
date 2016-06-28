
from django.test import TestCase, override_settings

from django_filters.conf import settings


class OverrideSettingsTests(TestCase):

    def test_attribute_override(self):
        self.assertIsInstance(settings.VERBOSE_LOOKUPS, dict)

        original = settings.VERBOSE_LOOKUPS

        with override_settings(FILTERS_VERBOSE_LOOKUPS=None):
            self.assertIsNone(settings.VERBOSE_LOOKUPS)

        self.assertIs(settings.VERBOSE_LOOKUPS, original)

    def test_non_filters_setting(self):
        self.assertFalse(hasattr(settings, 'USE_TZ'))

        with override_settings(USE_TZ=False):
            self.assertFalse(hasattr(settings, 'USE_TZ'))

        self.assertFalse(hasattr(settings, 'USE_TZ'))

    def test_non_existent_setting(self):
        self.assertFalse(hasattr(settings, 'FILTERS_FOOBAR'))
        self.assertFalse(hasattr(settings, 'FOOBAR'))

        with override_settings(FILTERS_FOOBAR='blah'):
            self.assertFalse(hasattr(settings, 'FILTERS_FOOBAR'))
            self.assertFalse(hasattr(settings, 'FOOBAR'))

        self.assertFalse(hasattr(settings, 'FILTERS_FOOBAR'))
        self.assertFalse(hasattr(settings, 'FOOBAR'))
