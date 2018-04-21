#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
  Python3 Music downloader based on Flask
  Copyright (C) 2017 MAIBACH ALAIN

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  Contact: alain.maibach@gmail.com / 34 rue appienne, 13480 Calas - FRANCE.
'''

from setuptools import setup

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
