#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   request_handler.py - the web application
#
#   PURPOSE: Serve web pages, handle javascript requests, and pass them on to
#   the serial deriver via RPC.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 8th August 2011
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

from flask import Flask, render_template, request, flash, jsonify
from flaskext.wtf import Form
from flaskext.wtf import validators as v
from custom_widgets import MultiCheckboxField

import sys
sys.path.append('../serial')
import serial_client

app = Flask(__name__)
# TODO make secret key more secret
app.secret_key = '''\xf9\xae!\xca\xae\x1a\xd6k\xf3\xd1\xc3\xb18~\xe2V"\x89=`q\xde\x91\xe4'''

##############################
# Helpers
##############################

# Generate random valve state; intended for testing only
from random import choice
random_state = lambda: ''.join([choice(['0', '1']) for i in range(8)])


# Categories of messages to flash
flash_categories = ['message', 'error']


# Convert data from a set of checkboxes in a form to the "binary state" string
to_bin = lambda data: ''.join(str(int(i in data)) for i in range(8))

##############################
# Web App
##############################

class ControlForm(Form):
    """ Provides an interface to control the microcontroller """
    a_state = MultiCheckboxField('Valves on port A',
            choices=[(i, str(i + 1)) for i in range(8)], coerce=int, default=[])
    b_state = MultiCheckboxField('Valves on port B',
            choices=[(i, str(i + 1)) for i in range(8)], coerce=int, default=[])
    k


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ControlForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        # TODO uncomment when actual hardware is available.
        # ret_a, ret_b = set_states(form.a_state.data, form.b_state.data)
        # flash(ret_a)
        # flash(ret_b)

        # convert to binary:
        a_state = to_bin(form.a_state.data)
        b_state = to_bin(form.b_state.data)
        flash("New states: %s & %s" % (a_state, b_state))
    html_form = render_template("_control_form.html", form=form)
    return render_template("index.html", html_form=html_form)


@app.route('/_set_states', methods=['POST'])
def set_states():
    """ AJAX-specific function to set the states """
    form = ControlForm(request.form, csrf_enabled=False)
    # TODO change this to actually call the actuation code and return more
    # useful feedback.
    if form.validate():
        a_state = to_bin(form.a_state.data)
        b_state = to_bin(form.b_state.data)
        code, feedback = serial_client.set_states(a_state, b_state)
        app.logger.debug(feedback)
        # flash, with category depending on success code of set_states call.
        flash(feedback, flash_categories[code > 0])
    else:
        app.logger.debug('Form did not validate. Request for A & B: %s %s', 
                a_state, b_state)
        flash("Invalid input.", "error")
    # Render partial template (just the form) and pass it back, including
    # errors and flashed messages (thanks to render_template magic)
    html_form = render_template("_control_form.html", form=form)
    return jsonify(html_form=html_form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
