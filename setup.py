#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='music_flask',
      version='0.0.1',
      author='Alain MAIBACH',
      author_email='alain.maibach@gmail.com',
      license='GPLv3',
      description='Make downloading music easier',
      packages=[
          'music_flask',
      ],
      include_package_data=True,
      install_requires=[
          'youtube_dl >= 2018.4.16',
          'Flask >= 0.12.2',
          'wtforms >= 2.1',
          'Flask-WTF >= 0.14.2'
      ],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'License :: GPL',
          'Programming Language :: Python :: 3 :: Only',
          'Environment :: Web Environment',
          'Topic :: Internet',
          'Topic :: Multimedia :: Sound/Audio',
      ])
