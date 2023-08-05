#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(
    name='drf-keyed-list-bihealth',
    version='0.1.1',
    url='http://github.com/bihealth/drf-keyed-list',
    license='Apache 2.0',
    description=('Fork of drf-keyed-list maintained by @bihealth'),
    install_requires=[
        "django>=3.0",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=('drf restframework rest_framework django_rest_framework'
              ' serializers drf_mapped_nested'),
    author='Manuel Holtgrewe, Mikko Nieminen, Oliver Stolpe',
    author_email='manuel.holtgrewe@bih-charite.de, mikko.nieminen@bih-charite.de, oliver.stolpe@bih-charite.de',
    packages=['drf_keyed_list'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
