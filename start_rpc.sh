#!/bin/bash
#
#  start_rpc.sh - Starts the RPyC registry server and the serial driver; only
#  intended for development.
#
#	AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#	DATE: 10 August 2011
#
########################################

DIR=/home/douglas/projects/microfluidics
# activate virtualenv
source $DIR/env/bin/activate

# Start RPyC registry server in the background
# Note: stopping it is a hack. Find the process id by running 
# `ps -elf | grep rpyc` 
python $DIR/env/bin/rpyc_registry.py &

# Start serial driver (just wait for a few seconds, for the registry to init.)
# cd serial/
# sleep 3
# python serial_driver.py
