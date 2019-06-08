from django.urls import reverse
from django.db import models
import os
from django.conf import settings
import datetime
from django.forms import TextInput, Textarea
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your models here.


def upper_ext(str):
    upper_map = {
        ord(u'ı'): u'I',
        ord(u'i'): u'İ',
    }
    return str.translate(upper_map).upper()


def model_format(model, format):
    map = model_to_dict(model)
    return format.format(**map)


class EventType(models.Model):
    code = models.CharField(max_length=100, default='',
                            blank=True, verbose_name=_('Code'), unique=True)  # type
    title = models.CharField(max_length=100, default='',
                             blank=True, verbose_name=_('Title'))  # type

    def save(self, *args, **kwargs):
        self.code = upper_ext(self.code)
        self.title = upper_ext(self.title)
        super(EventType, self).save(*args, **kwargs)

    def __str__(self):
        # fo use in model-select-filed
        return self.code
        #map = model_to_dict(self)
        # return self._meta.verbose_name + ': {code} / {title}'.format(**map)

    class Meta:
        verbose_name = 'Event Type'


class EventRecord(models.Model):

    specode = models.CharField(
        max_length=100, default='', blank=True,
        verbose_name=_('Type'),
    )

    # specode = models.ForeignKey(EventType,
    #                             blank=True, null=True,
    #                             db_column='specode',
    #                             to_field='code',
    #                             on_delete=models.DO_NOTHING)

    recdate = models.DateField(
        default=datetime.date.today, blank=True, verbose_name=_('Date'))  # date
    duedate = models.DateField(
        default=datetime.date.today, blank=True, verbose_name=_('Due Date'))  # duedate

    textf1 = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Object Name'))
    textf2 = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Task Title'))
    textf3 = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Task From'))
    textf4 = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Task Executor'))

    STATUS0 = 0
    STATUS1 = 1
    STATUS_CHOICES = [
        (STATUS0, ''),
        (STATUS1, 'İcra O.'),
    ]

    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS0,
        blank=False,
        verbose_name=_('Status')
    )

    formated = None

    # description = models.TextField()
    # technology = models.CharField(max_length=20)

    #_meta = None

    def __str__(self):

        if self.formated:
            return self.formated

        return model_format(self, self._meta.verbose_name + ': Nr: {id}, Type: {specode}, Title: {textf2}')

    def get_absolute_url(self):
        return reverse('eventrecord_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = _('Event Record')
        verbose_name_plural = _('Event Records')
        # permissions = (("can_mark_returned", "Set book as returned"),)
        pass
    #     ordering = ['-id']
