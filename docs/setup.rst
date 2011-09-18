Setup
=====

This guide covers setup on Ubuntu Linux (10.10 or 11.04). Muigi should work on
most Debian derivatives, but is not designed to work on any other system. The
python part should work alright, but the `init` scripts for the servers are
platform-specific. If you are trying to port this to another platform, start by
looking at the ``setup.py`` file, specifically at the 'scripts'.

On Ubuntu, setup is relatively straightforward. First, install the two
dependencies::

    sudo apt-get install python-setuptools redis-server

Setuptools are required for the ``setup.py`` script to work. Redis is used by the
web application.

The next step is to run the ``setup.py`` script::

    sudo python setup.py install

This will install the python ``muigi`` package, as well as init scripts for all
the services used: the RPyC registry, the Muigi web server (based on CherryPy)
and the Tamagotchip RPC server.

Finally, run the post_install.sh script::

    sudo scripts/post_install.sh

All this does is registers the previously-mentioned init scripts, so that
Muigi Web is launched on startup.
