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

from __future__ import unicode_literals

import os
import youtube_dl
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory

__author__ = "Alain Maibach"
__status__ = "Developement"

class MyLogger(object):
    """
      Wiiz
    """
    def debug(self, msg):
        """
          Wizz
        """
        pass

    def warning(self, msg):
        """
          Wizz
        """
        pass

    def error(self, msg):
        """
          Wizz
        """
        print(msg)

def my_hook(_d):
    """
      Wizz
    """

    if _d['status'] == 'finished':
        print('Done downloading, now converting ...')

def show_main_page():
    """
      This function render the main page after a sucessfull log in.
    """
    return render_template('main.html')

def youtube_download(url):
    """
      This function will handles authentication mecanisme
    """

    data_dir = os.path.join(APP.root_path, 'data')
    ydl_opts = {
        'format': 'bestaudio/best',
        'geo-bypass': True,
        'no-playlist': True,
        'restrict-filenames': True,
        'retries': 10,
        'fragment-retries': 10,
        'continue': True,
        'no-part': True,
        'no-cache-dir': True,
        'rm-cache-dir': True,
        'add-metadata': True,
        'embed-thumbnail': True,
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64)
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36''',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'outtmpl': '{}/%(title)s.%(ext)s'.format(data_dir)
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "OK"

APP = Flask(__name__)

@APP.route('/', methods=['GET', 'POST'])
def main_page():
    """
      Login func which serves the main page
    """

    if request.method == 'POST':
        url = request.form['URL']
        return youtube_download(url)

    if request.method == 'GET':
        return show_main_page()

    return show_main_page()

@APP.route('/music')
def list_music():
    """
    wizz
    """

    musics = []
    directories = []
    main_paths = []
    data_dir = os.path.join(APP.root_path, 'data')

    for root, dirs, files in os.walk(data_dir):
        main_paths.append(root)
        directories.append(dirs)
        for filename in [name for name in files]:
            if not filename.endswith('.mp3'):
                continue
            musics.append(filename)
    return render_template('music.html', musics=musics)

@APP.route('/music/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    """
    wiiiz
    """
    data_dir = os.path.join(APP.root_path, 'data')
    response = send_from_directory(directory=data_dir, filename=filename)
    response.headers['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    response.headers['Content-Type'] = 'audio/mpeg'
    return response

if __name__ == '__main__':
    APP.run(debug=True, host='127.0.0.1', port=8080)
