##
#     Project: Django Admin Settings
# Description: A Django application to configure some Django Admin settings
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2023 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from django.contrib import admin
from django.db import models
from django.utils.translation import pgettext_lazy

from ..forms import ModelChoicesForm


class ListDisplayLink(models.Model):
    """
    List Display Link
    """
    model = models.CharField(
        max_length=255,
        verbose_name=pgettext_lazy('ListDisplayLink', 'model'))
    field = models.CharField(
        max_length=255,
        verbose_name=pgettext_lazy('ListDisplayLink', 'field'))
    order = models.PositiveIntegerField(
        verbose_name=pgettext_lazy('ListDisplayLink', 'order'))
    is_active = models.BooleanField(
        default=True,
        verbose_name=pgettext_lazy('ListDisplayLink', 'is_active'))

    class Meta:
        ordering = ['model', 'order', 'field']
        unique_together = (('model', 'field'),
                           ('model', 'order'))
        verbose_name = pgettext_lazy('ListDisplayLink',
                                     'List Display Link')
        verbose_name_plural = pgettext_lazy('ListDisplayLink',
                                            'List Display Links')

    def __str__(self):
        return '{MODEL} - {FIELD}'.format(MODEL=self.model,
                                          FIELD=self.field)


class ListDisplayLinkAdmin(admin.ModelAdmin):
    """
    List Display Link admin
    """
    form = ModelChoicesForm
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active', )
