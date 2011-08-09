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
from flaskext.wtf import Form, TextField
from flaskext.wtf import validators as v

import sys
sys.path.append('../serial')
from serial_client import set_states

app = Flask(__name__)
# TODO make secret key more secret
app.secret_key = '''\xf9\xae!\xca\xae\x1a\xd6k\xf3\xd1\xc3\xb18~\xe2V"\x89=`q\xde\x91\xe4'''

from random import choice
random_state = lambda: ''.join([choice(['0', '1']) for i in range(8)])

class ControlForm(Form):
    a_state = TextField('State of port A', default=random_state(),
            validators=[v.Required(), v.Length(min=8, max=8)])
    b_state = TextField('State of port B', default=random_state(),
            validators=[v.Required(), v.Length(min=8, max=8)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ControlForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        ret_a, ret_b = set_states(form.a_state.data, form.b_state.data)
        flash(ret_a)
        flash(ret_b)
    return render_template("index.html", form=form)

@app.route('/_set_states', methods=['POST'])
def set_states():
    """ AJAX-specific function to set the states """
    a_state = request.form['a_state']
    b_state = request.form['b_state']
    # TODO change this to actually call the actuation code and return more
    # useful feedback.
    app.logger.debug('A & B states set to: %s %s', a_state, b_state)
    return jsonify(feedback="A set to %s and B set to %s" % (a_state,
        b_state), new_a=random_state(), new_b=random_state())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
