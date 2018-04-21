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
from __core__ import Core

__author__ = "Alain Maibach"
__status__ = "Developement"

PYTHON3 = sys.version_info.major == 3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]

# Instanciate flask
APP = Flask(__name__)

# Protect flask app with CSRF giving secret keys
APP_CSRF = CSRFProtect(APP)
APP.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# Load music_flask core tools
MUSIC_CORE = Core(app=APP, data_dir=False)

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
            return MUSIC_CORE.youtube_download(urls=urls)

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
    return render_template('music.html', musics=musics, pagename='musics')

@APP.route('/music/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    """
    wiiiz
    """
    # ici changer l'appel a data dir pour creer une func dans la class qui retourne sa valeur
    response = send_from_directory(directory=MUSIC_CORE.data_dir, filename=filename)
    response.headers['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    response.headers['Content-Type'] = 'audio/mpeg'
    return response

if __name__ == '__main__':
    APP.run(debug=False, host='0.0.0.0', port=1080)
