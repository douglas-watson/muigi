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

import time

from flask import Flask, render_template, request, flash, jsonify, session, \
    redirect, url_for
from flaskext.wtf import Form
from flaskext.wtf import validators as v
from custom_widgets import MultiCheckboxField

from redis import Redis
from kronos import ThreadedScheduler, method

from flask_secrets import secret_key
from muigi.hardware import lbnc_client as serial_client

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
# Reverse a string
reverse = lambda s: s[-1::-1]

# TODO write a "get id" helper, that returns the session id, or creates a new
# one if necessary (if id doesn't exist, or is outdated)

def heartbeat(id):
    ''' Update "last_seen" line in Redis for the given id. '''
    r.zadd('last_seen', **{id:time.time()})
    return 'OK'

def remove_inactive():
    ''' Delete inactive users from the waiting line. '''

    for oldie in r.zrangebyscore('last_seen', 0, time.time() - app.usertimeout):
        r.zrem('waiting_line', oldie)
        r.zrem('last_seen', oldie)

def get_waiting_time(id):
    ''' Return estimated waiting time for a user in the queue. Id is the
    user id, as a string.

    '''

    # TODO get remaining playing time for current player (this is a fake)
    remaining_time = app.playingtime - time.time() % app.playingtime
    pos = r.zrank('waiting_line', id)
    return pos * app.playingtime + remaining_time

##############################
# Setup 
##############################

app = Flask(__name__)
# TODO make secret key more secret
app.secret_key = secret_key

# Redis database stores the following data:
# 
# usercount - an integer, incremented each time a user logs in. Current value
#   used as a user id.
# waiting_line - an ordered list, where the score is login time. A disconnected
#   user is removed from the list
# last_seen - an ordered list, with user id as value and time of last heartbeat
#   as score
r = Redis('localhost')
app.usertimeout = 10    # seconds after which a user is kicked out
app.playingtime = 10    # seconds of playing time per session
app.purgeinterval = 5   # seconds after which the waiting line is purged

# Every x seconds, delete inactive users from the waiting line.
app.scheduler = ThreadedScheduler()
app.scheduler.add_interval_task(remove_inactive, 'remove_inactive',
                                app.purgeinterval, app.purgeinterval,
                                method.threaded, None, None)



##############################
# Views
##############################

class ControlForm(Form):
    """ Provides an interface to control the microcontroller """
    a_state = MultiCheckboxField('Valves on port A',
            choices=[(i, str(i + 1)) for i in range(8)], coerce=int, default=[])
    b_state = MultiCheckboxField('Valves on port B',
            choices=[(i, str(i + 1)) for i in range(8)], coerce=int, default=[])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ControlForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        # TODO uncomment when actual hardware is available.
        a_state = reverse(to_bin(form.a_state.data))
        b_state = reverse(to_bin(form.b_state.data))
        code, feedback = serial_clientset_states(a_state, b_state)

        flash(feedback, flash_categories[code > 0])

    html_form = render_template("_control_form.html", form=form)

    return render_template("index.html", html_form=html_form)

@app.route('/_set_states', methods=['POST'])
def set_states():
    """ AJAX-specific function to set the states """
    form = ControlForm(request.form, csrf_enabled=False)
    if form.validate():
        a_state = reverse(to_bin(form.a_state.data))
        b_state = reverse(to_bin(form.b_state.data))
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

@app.route('/spectator')
def spectator():
    session.permanent = False
    if not 'id' in session or ('id' in session and session['id'] == -1
                          or r.zrank('waiting_line', session['id']) is None): 
        # Session is new or 'deleted'. create user and register to waiting line
        id = str(r.incr('usercount'))
        session['id'] = id
        r.zadd('waiting_line', **{id:time.time()})
        r.zadd('last_seen', **{id:time.time()})

    return render_template("spectator.html")

@app.route('/_player_heartbeat')
def player_update():
    ''' Update 'last seen' for a player. '''

    id = session['id']
    heartbeat(id)

    return 'OK'

@app.route('/_get_position')
def get_position():
    ''' Return position in line and waiting time. Also logs 'heartbeat'. '''
    id = session['id']
    data = {}

    heartbeat(id)

    pos = int(r.zrank('waiting_line', id) + 1)
    data['position'] = pos
    data['wait'] = int(get_waiting_time(id))

    if pos == 1:
        data['status'] = "player"
        form = ControlForm(request.form, csrf_enabled=False)
        data['form']= render_template("_control_form.html", form=form)
    else:
        data['status'] = "spectator"

    return jsonify(**data)



@app.route('/_quit', methods=['POST'])
def quit():
    ''' Remove user from waiting line. Called when a user leaves the page. '''

    id = session['id']
    r.zrem('waiting_line', id)
    r.zrem('last_seen', id)
    session['id'] = -1 # marks it a 'deleted' session

    return 'OK'

@app.route('/_get_users')
def get_users():
    ''' Return list of logged in users. '''
    return jsonify(redis_last=r.zrange('last_seen', 0, -1, withscores=True), 
                  redis_wait=r.zrange('waiting_line', 0, -1, withscores=True))

@app.route('/_get_info')
def get_info():
    ''' Returns session info about the logged in user. '''
    id = session['id']
    app.logger.debug(session.clear.__doc__)

    return jsonify(id=id, login=r.zscore('waiting_line', id), 
                   last_seen=r.zscore('last_seen', id))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.scheduler.start()
    app.run(debug=True, host='0.0.0.0')
    app.scheduler.stop()
