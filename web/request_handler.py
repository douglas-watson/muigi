#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   request_handler.py - the web framework 
#
#   PURPOSE: Serve web pages, handle javascript requests, and pass them on to
#   the serial deriver via RPC.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 8th August 2011
#
#   LICENSE: GNU GPL
#
#################################################

from flask import Flask, render_template, request, flash, jsonify
from flaskext.wtf import Form, TextField, SelectMultipleField
from flaskext.wtf import validators as v
from custom_widgets import MultiCheckboxField

import sys
sys.path.append('../serial')
from serial_client import set_states

app = Flask(__name__)
# TODO make secret key more secret
app.secret_key = '''\xf9\xae!\xca\xae\x1a\xd6k\xf3\xd1\xc3\xb18~\xe2V"\x89=`q\xde\x91\xe4'''

from random import choice
random_state = lambda: ''.join([choice(['0', '1']) for i in range(8)])

class ControlForm(Form):
    a_state = MultiCheckboxField('Valves on port A',
            choices=[(i, str(i + 1)) for i in range(8)], coerce=int, default=[])
    b_state = MultiCheckboxField('Valves on port B',
            choices=[(i, str(i + 1)) for i in range(8)], coerce=int, default=[])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ControlForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        # TODO uncomment when actual hardware is available.
        # ret_a, ret_b = set_states(form.a_state.data, form.b_state.data)
        # flash(ret_a)
        # flash(ret_b)

        # convert to binary:
        to_bin = lambda data:''.join(str(int(i in data)) for i in range(8)) 
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
        to_bin = lambda data:''.join(str(int(i in data)) for i in range(8)) 
        a_state = to_bin(form.a_state.data)
        b_state = to_bin(form.b_state.data)
        app.logger.debug('A & B states set to: %s %s', a_state, b_state)
        flash("New states: %s & %s" % (a_state, b_state))
    else:
        app.logger.debug('Erroneous request for A & B: %s %s', a_state,
                b_state)
        flash("Invalid input")
    html_form = render_template("_control_form.html", form=form)
    return jsonify(html_form=html_form, new_a=random_state(), 
            new_b=random_state())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
