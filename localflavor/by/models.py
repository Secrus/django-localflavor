from django.db.models import CharField
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _

from .by_regions import BY_REGIONS_CHOICES
from .forms import BYRegionField as BYRegionFormField
from .forms import BYPassNumberField as BYPassNumberFormField
from .forms import BYPassIdNumberField as BYPassIdNumberFormField
from .forms import ByZIPCodeField as BYZIPCodeFormField
from .validators import (
    PASS_NUMBER_VALIDATOR, PASS_ID_NUMBER_VALIDATOR,
)


class BaseModelFieldUpdated:
    """
    Abstract base class made to conform the DRY principle.

    The initial_options is overrided by the dict in the subclasses and then
    automatically passed to kwargs in the ModelField.__init__() method.
    After, the parameters defined in the initial_options are deleted in
    the ModelField.deconstruct() method.
    """

    initial_options = None

    def __init__(self, *args, **kwargs):
        kwargs.update(self.initial_options)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for field in self.initial_options.keys():
            if field != 'max_length':
                del kwargs[field]
        return name, path, args, kwargs


class BYRegionField(BaseModelFieldUpdated, CharField):
    """
    A model field that stores the numbers representing Belarusian regions.

    The regional data is stored in ``by_regions.BY_REGIONS_CHOICES``.

    Form represents it as a ``forms.BYRegionField`` field.
    """

    description = _('Belarusian Regions (one integer value in range 1-7).')
    initial_options = {
        'choices': BY_REGIONS_CHOICES,
        'max_length': 1,
    }

    def formfield(self, **kwargs):
        defaults = {'choices_form_class': BYRegionFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class BYPassNumberField(BaseModelFieldUpdated, CharField):
    """
    A model field that stores the number of Belarusian passport.

    Form represents it as a ``forms.BYPassNumberField`` field.
    """

    description = _('Belarusian passport number (2 letters followed by 7 digits')
    initial_options = {
        'max_length': 9,
        'validators': (PASS_NUMBER_VALIDATOR, )
    }

    def formfield(self, **kwargs):
        defaults = {'form_class': BYPassNumberFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class BYPassIdNumberField(BaseModelFieldUpdated, CharField):
    """
    A model field that stores the ID number.

    Form represents it as a ``forms.BYPassIdNumberField`` field.
    """

    description = _('Belarusian passport ID number (14 letters and digits).')
    initial_options = {
        'max_length': 14,
        'validators': (PASS_ID_NUMBER_VALIDATOR, )
    }

    def formfield(self, **kwargs):
        defaults = {'form_class': BYPassIdNumberFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class BYZIPCodeField(BaseModelFieldUpdated, CharField):
    """
    A model field that stores Belarusian ZIP code.

    Form represents it as a ``forms.BYZIPCodeField`` field.
    """

    description = _('Belarusian ZIP code (6 digits).')

    initial_options = {
        'max_length': 6,
        'validators': (MinLengthValidator(6), )
    }

    def formfield(self, **kwargs):
        defaults = {'form_class': BYZIPCodeFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
