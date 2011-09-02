#!/usr/bin/env python
# -*- coding: UTF8 -*-

from setuptools import setup

setup(
    name='Muigi the Microplumber',
    version='0.1a',
    long_description=__doc__,
    packages=['muigi', 
              'muigi.web', 
              'muigi.serial'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 
                      'Flask-WTF', 
                      'Flask-Celery',
                      'pyserial',
                      'RPyC',
                      'redis',
                     ]
)
