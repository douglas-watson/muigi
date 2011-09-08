#!/usr/bin/env python
# -*- coding: UTF8 -*-

from setuptools import setup

import muigi
    
setup(
    name='Muigi the Microplumber',
    version=muigi.__version__,
    description="Framework to control microfluidic games from the web",
    long_description=muigi.__doc__,
    platforms=['POSIX'],
    packages=['muigi', 
              'muigi.web', 
              'muigi.hardware',
              'muigi.applications'],
    scripts=['scripts/muigi-production-server'],
    data_files=[
        ('/etc/init.d/', 'scripts/rpyc-registry'),
        ('/etc/init.d/', 'scripts/muigi-web'),
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 
                      'flask-wtf', 
                      'pyserial',
                      'RPyC',
                      'redis',
                     ],
    test_suite='nose.collector',
    test_requires=['Nose'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: System :: Hardware',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
)
