#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   custom_widgets.py - custom widgets for Flask 
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 9th August 2011
#
#   LICENSE: GNU GPLv3
#
#   Copyright (C) 2011 Douglas Watson
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################

from flaskext.wtf import SelectMultipleField, widgets
from cgi import escape

# Can't import HTMLString or html_params, so I have to copy-paste the source code here...
def html_params(**kwargs):
    """
    Generate HTML parameters from inputted keyword arguments.

    The output value is sorted by the passed keys, to provide consistent output
    each time this function is called with the same parameters.  Because of the
    frequent use of the normally reserved keywords `class` and `for`, suffixing
    these with an underscore will allow them to be used.

    >>> html_params(name='text1', id='f', class_='text')
    u'class="text" id="f" name="text1"'
    """
    params = []
    for k,v in sorted(kwargs.iteritems()):
        if k in ('class_', 'class__', 'for_'):
            k = k[:-1]
        if v is True:
            params.append(k)
        else:
            params.append(u'%s="%s"' % (unicode(k), 
                escape(unicode(v), quote=True)))
    return u' '.join(params)

class HTMLString(unicode):
    def __html__(self):
        return self

##############################
# BEGIN CUSTOM WIDGETS 
##############################

class SingleRowTable(object):
    """
    Renders a list of fields in a signle row, where each cell contains the
    label and the field. To display the label above the field, use the
    following css style, to ensure a newline after the label:

        td label { display: block } 

    If `with_table_tag` is True, then an enclosing <table> is placed around the
    rows.

    Hidden fields will not be displayed with a row, instead the field will be 
    pushed into a subsequent table row to ensure XHTML validity. Hidden fields
    at the end of the field list will appear outside the table.

    This is a re-write of the TableWidget code from the original WTForms:
    https://bitbucket.org/simplecodes/wtforms/src/8335f03e547c/wtforms/widgets/core.py
    """
    def __init__(self, with_table_tag=True):
        self.with_table_tag = with_table_tag

    def __call__(self, field, **kwargs):
        html = []
        if self.with_table_tag:
            kwargs.setdefault('id', field.id)
            html.append(u'<table %s><tr>' % html_params(**kwargs))
        hidden = u''
        for subfield in field:
            if subfield.type == 'HiddenField':
                hidden += unicode(subfield)
            else:
                html.append(u'<td>%s%s%s</td>' % 
                        (unicode(subfield.label), hidden, unicode(subfield)))
                hidden = u''
        if self.with_table_tag:
            html.append(u'</tr></table>')
        if hidden:
            html.append(hidden)
        return HTMLString(u'\n'.join(html))

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = SingleRowTable()
    option_widget = widgets.CheckboxInput()

