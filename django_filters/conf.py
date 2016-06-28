
from django.core.signals import setting_changed
from django.utils.translation import ugettext_lazy as _


DEFAULTS = {
    'VERBOSE_LOOKUPS': {
        # transforms don't need to be verbose, since their expressions are chained
        'date': _('date'),
        'year': _('year'),
        'month': _('month'),
        'day': _('day'),
        'week_day': _('week day'),
        'hour': _('hour'),
        'minute': _('minute'),
        'second': _('second'),

        # standard lookups
        'exact': _(''),
        'iexact': _(''),
        'contains': _('contains'),
        'icontains': _('contains'),
        'in': _('is in'),
        'gt': _('is greater than'),
        'gte': _('is greater than or equal to'),
        'lt': _('is less than'),
        'lte': _('is less than or equal to'),
        'startswith': _('starts with'),
        'istartswith': _('starts with'),
        'endswith': _('ends with'),
        'iendswith': _('ends with'),
        'range': _('is in range'),
        'isnull': _(''),
        'regex': _('matches regex'),
        'iregex': _('matches regex'),
        'search': _('search'),

        # postgres lookups
        'contained_by': _('is contained by'),
        'overlap': _('overlaps'),
        'has_key': _('has key'),
        'has_keys': _('has keys'),
        'has_any_keys': _('has any keys'),
        'trigram_similar': _('search'),
    },
}


class Settings(object):

    def __init__(self):
        from django.conf import settings

        for setting in DEFAULTS.keys():
            value = getattr(settings, 'FILTERS_%s' % setting, DEFAULTS[setting])
            setattr(self, setting, value)

    def VERBOSE_LOOKUPS():
        """
        VERBOSE_LOOKUPS accepts a dictionary of {terms: verbose expressions}
        or a zero-argument callable that resolves to a dictionary.
        """
        def fget(self):
            if callable(self._VERBOSE_LOOKUPS):
                self._VERBOSE_LOOKUPS = self._VERBOSE_LOOKUPS()
            return self._VERBOSE_LOOKUPS

        def fset(self, value):
            self._VERBOSE_LOOKUPS = value

        return locals()
    VERBOSE_LOOKUPS = property(**VERBOSE_LOOKUPS())

    def change_setting(self, setting, value, **kwargs):
        if setting.startswith('FILTERS_'):
            setting = setting[8:]  # strip 'FILTERS_'

            if hasattr(self, setting):
                setattr(self, setting, value)


settings = Settings()
setting_changed.connect(settings.change_setting)
