#!/usr/bin/env python
# -*- coding: UTF8 -*-

from setuptools import setup

import muigi
    
setup(
    name='Muigi the Microplumber',
    version='0.1a',
    long_description=muigi.__doc__,
    packages=['muigi', 
              'muigi.web', 
              'muigi.hardware',
              'muigi.applications'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 
                      'Flask-WTF', 
                      'Flask-Celery',
                      'pyserial',
                      'RPyC',
                      'redis',
                     ],
    test_suite='nose.collector',
    test_requires=['Nose'],
)
