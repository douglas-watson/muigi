#!/bin/bash
# Just registers the two init.d scripts

update-rc.d muigi-web defaults
update-rc.d rpyc-registry defaults
update-rc.d tamagotchip-server defaults

