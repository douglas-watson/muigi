#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   cherrypy_server.py - Serve the web application through CherryPy's web
#   server.
#
#   PURPOSE: Easily deploy the web app on a production-grade server, without
#   the hassle of configuring Apache and the like.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 11 August 2011
#
#   LICENSE: GNU GPL
#
#################################################

from cherrypy import wsgiserver
from request_handler import app

PORT=8080
HOST='0.0.0.0'

d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
server = wsgiserver.CherryPyWSGIServer((HOST, PORT), d)

if __name__ == '__main__':
    try:
        print "Server running on %s:%s" % (HOST, PORT) 
        server.start()
    except KeyboardInterrupt:
        server.stop()
