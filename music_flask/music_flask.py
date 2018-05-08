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
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import url_for
from flask import redirect
from flask import flash
from flask_wtf.csrf import CSRFProtect

from forms import RequiredField

import urllib.parse

from __core__ import Core

__author__ = "Alain Maibach"
__status__ = "Developement"

PYTHON3 = sys.version_info.major == 3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]

TLS = False
TLS_CERTIFICATE = ''
TLS_KEY = ''
PORT = 1080
LISTEN = "0.0.0.0"
DEBUG = False
CSRF_KEY = "powerful secretkey"
CSRF_FORM_TOKEN = "a csrf secret key"
DATA_DIRECTORY = False

if __name__ == '__main__':
    # Instanciate flask
    APP = Flask(__name__)

    # Protect flask app with CSRF giving secret keys
    APP_CSRF = CSRFProtect(APP)
    APP.config.update(dict(
        SECRET_KEY=CSRF_KEY,
        WTF_CSRF_SECRET_KEY=CSRF_FORM_TOKEN
    ))

    # Load music_flask core tools
    MUSIC_CORE = Core(app=APP, data_dir=DATA_DIRECTORY)

    @APP.route('/', methods=['GET', 'POST'])
    def main_page():
        """
          This, serves the main page
        """
        if request.method == 'POST':
            form = RequiredField()
            if form.validate_on_submit():
                urls = request.form['URL'].split(' ')

                encoded_urls = []
                for url in urls:
                    encoded_url = urllib.parse.quote(url)
                    encoded_urls.append(encoded_url)

                return MUSIC_CORE.youtube_download(urls=encoded_urls)

            flash('Please fill the URL before submitting', 'warning')
            return redirect(url_for('main_page'))

        if request.method == 'GET':
            return MUSIC_CORE.show_main_page()

        return MUSIC_CORE.show_main_page()

    @APP.route('/music')
    def list_music():
        """
        wizz
        """

        musics = MUSIC_CORE.list_mp3()
        return render_template('music.html',
                               musics=musics,
                               pagename='musics',
                               app_version=MUSIC_CORE.app_version
                              )

    @APP.route('/music/<path:filename>', methods=['GET', 'POST'])
    def download_file(filename):
        """
        wiiiz
        """
        response = send_from_directory(directory=MUSIC_CORE.data_dir, filename=filename)
        response.headers['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
        response.headers['Content-Type'] = 'audio/mpeg'
        return response

    if not TLS:
        APP.run(debug=DEBUG, host=LISTEN, port=PORT)
    else:
        if not TLS_CERTIFICATE and not TLS_KEY:
            APP.run(debug=DEBUG, host=LISTEN, port=PORT, ssl_context='adhoc')
        else:
            if not TLS_CERTIFICATE:
                print('Missing TLS certificate file path')
                del MUSIC_CORE
                del APP
                exit(1)
            if not TLS_KEY:
                print('Missing TLS private key path')
                del MUSIC_CORE
                del APP
                exit(1)

            if not os.path.isfile(TLS_CERTIFICATE):
                print('Unable to find certificate file {}'.format(TLS_CERTIFICATE))
                del MUSIC_CORE
                del APP
                exit(1)

            if not os.path.isfile(TLS_KEY):
                print('Unable to find private key file {}'.format(TLS_KEY))
                del MUSIC_CORE
                del APP
                exit(1)

            APP.run(debug=DEBUG, host=LISTEN, port=PORT, ssl_context=(TLS_CERTIFICATE, TLS_KEY))

    del MUSIC_CORE
    del APP
    exit(0)
