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
import sys
import youtube_dl
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import url_for
from flask import redirect
from flask import flash
from flask_wtf.csrf import CSRFProtect

from forms import RequiredField

__author__ = "Alain Maibach"
__status__ = "Developement"

PYTHON3 = sys.version_info.major == 3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]

class MyLogger(object):
    """
      Wiiz
    """
    def __init__(self):
        self.__error = 0
        self.__warning = 0
        self.__debug = 0

    def debug(self, msg):
        """
          Wizz
        """
        self.__debug = 1
        print(msg)

    def warning(self, msg):
        """
          Wizz
        """
        self.__warning = 1
        print(msg)

    def error(self, msg):
        """
          Wizz
        """
        self.__error = 1
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
    return render_template('main.html', pagename='download')

def youtube_download(urls, destination=False):
    """
      This function will handles authentication mecanisme
    """

    if not destination:
        data_dir = os.path.join(APP.root_path, 'data')
    else:
        data_dir = str(destination)
    ydl_opts = {
        'format': 'bestaudio/best',
        'geo-bypass': True,
        'no-playlist': True,
        'restrict-filenames': True,
        'retries': 10,
        'fragment-retries': 10,
        'continue': True,
        'no-overwrites': True,
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
        #for url in urls:
        #    try:
        #        ydl.download([url])
        try:
            ydl.download(urls)
        except youtube_dl.DownloadError as err:
            flash('Failed to download: {}'.format(str(err)), 'error')
            return redirect(url_for('main_page'))
        except youtube_dl.SameFileError as err:
            flash('Same file already downloaded: {}'.format(str(err)), 'error')
            return redirect(url_for('main_page'))
        except youtube_dl.utils.ExtractorError as err:
            flash('Extracting error: {}'.format(str(err)), 'error')
            return redirect(url_for('main_page'))
        except youtube_dl.utils.UnavailableVideoError as err:
            flash('Video not available on requested url: {}'.format(str(err)), 'error')
            return redirect(url_for('main_page'))

    str_urls = "\n".join(urls)
    flash(r'{} Downloaded'.format(str_urls), 'info')
    return redirect(url_for('list_music'))

# Instanciate flask
APP = Flask(__name__)

# Protect flask app with CSRF giving secret keys
APP_CSRF = CSRFProtect(APP)
APP.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

@APP.route('/', methods=['GET', 'POST'])
def main_page():
    """
      This, serves the main page
    """
    if request.method == 'POST':
        form = RequiredField()
        if form.validate_on_submit():
            #urls = []
            #urls.append(request.form['URL'])
            urls = request.form['URL'].split(' ')
            return youtube_download(urls=urls)

        flash('Please fill the URL before submitting', 'warning')
        return redirect(url_for('main_page'))

    if request.method == 'GET':
        return show_main_page()

    return show_main_page()

@APP.route('/music')
def list_music(destination=False):
    """
    wizz
    """

    musics = []
    directories = []
    main_paths = []
    if not destination:
        data_dir = os.path.join(APP.root_path, 'data')
    else:
        data_dir = str(destination)

    for root, dirs, files in os.walk(data_dir):
        main_paths.append(root)
        directories.append(dirs)
        for filename in [name for name in files]:
            if not filename.endswith('.mp3'):
                continue
            musics.append(filename)
    return render_template('music.html', musics=musics, pagename='musics')

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
    APP.run(debug=False, host='0.0.0.0', port=1080)
