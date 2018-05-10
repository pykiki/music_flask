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
import signal
import time
import youtube_dl
from flask import render_template
from flask import flash
from flask import url_for
from flask import redirect
from __logger__ import MyLogger
import __chk_disk__

__author__ = "Alain Maibach"
__status__ = "Developement"

PYTHON3 = sys.version_info.major == 3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
APP_VERSION = 'v1.1.2'

class Core(object):
    ''' Core class which contains music_flask engine functions '''

    def __init__(self, app, data_dir=False):
        ''' '''

        self.__flask_app = app
        if not data_dir:
            self.__data_dir = os.path.join(self.__flask_app.root_path, 'data')
        else:
            self.__data_dir = str(data_dir)

        self.__main_page_name = 'download'
        self.__main_html_file = 'main.html'
        self.__app_version = APP_VERSION
        self.__iserr = False

        self.__t_zero = time.process_time()
        self.__progress_percent = 0

        self.__code = False
        self.__interrupt = False
        signal.signal(signal.SIGINT, self.sigint_handler)

    def __del__(self):
        pass

    def sigint_handler(self, signum, frame):
        '''
         Class sig handler for ctrl+c interrupt
        '''

        self.__code = signum
        self.__interrupt = frame
        print("Execution interrupted by pressing [CTRL+C]")
        del self.__flask_app
        exit(0)

    def my_hook(self, data):
        """
          Wizz
        """

        if data['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(data['filename']))
            file_name = file_tuple[1]
            #elapsed_time = time.perf_counter() - self.__t_zero
            self.__progress_percent = 100

        if data['status'] == 'downloading':
            if data['downloaded_bytes'] == 0:
                # Initial call to print 0% progress
                self.__progress_percent = 0
            else:
                file_tuple = os.path.split(os.path.abspath(data['filename']))
                file_dir = file_tuple[0]
                file_name = file_tuple[1]
                free_space = __chk_disk__.path_freespace(file_dir)
                if 'total_bytes_estimate' in data and data['total_bytes_estimate']:
                    if data['total_bytes_estimate'] > free_space['bytes']:
                        raise ValueError(
                            'Failed to download file {}, no space left on disk.'.format(file_name)
                            )

                if data['total_bytes']:
                    self.__progress_percent = 100 * data['downloaded_bytes'] / data['total_bytes']
        #return self.__progress_percent

    def show_main_page(self):
        """
          This function render the main page after a sucessfull log in.
        """
        return render_template(self.__main_html_file,
                               pagename=self.__main_page_name,
                               app_version=self.__app_version
                              )

    def url_get_infos(self, url, youtube_opts):
        """ Wiiiiz """
        ydl = youtube_dl.YoutubeDL(youtube_opts)
        infos = None
        try:
            infos = ydl.extract_info(url, process=False, download=False)
        except youtube_dl.utils.UnavailableVideoError as err:
            self.__iserr = True
            print(err)
            return False
        except youtube_dl.DownloadError as err:
            self.__iserr = True
            print(err)
            return False
        except youtube_dl.SameFileError as err:
            self.__iserr = True
            print(err)
            return False
        except youtube_dl.utils.ExtractorError as err:
            self.__iserr = True
            print(err)
            return False

        return infos

    def youtube_download(self, urls):
        """
          This function will handles authentication mecanisme
        """

        unix_friendly_names = True

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'restrictfilenames': unix_friendly_names,
            'nooverwrites': True,
            'nopart': True,
            'cachedir': False,
            'geo_bypass': True,
            'writethumbnail': False,
            'writeinfojson': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.my_hook],
            'outtmpl': '{}/%(title)s.%(ext)s'.format(self.__data_dir),
            'continuedl': True,
            'retries': 10
        }

        not_found = []
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            for url in urls:
                info = self.url_get_infos(url=url, youtube_opts=ydl_opts)
                if not info:
                    urls.remove(url)
                    not_found.append(url)
                    continue

                try:
                    self.__progress_percent = 0
                    self.__t_zero = time.perf_counter()
                    ydl.download([url])
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

                flash('The music {} with a Youtube ID {} has been downloaded..'.
                      format(info['title'],
                             info['id']
                            ),
                      'info'
                     )

        if not_found:
            for url_err in not_found:
                flash("{} has not been found on Youtube\n".
                      format(url_err),
                      'error'
                     )

        return redirect(url_for('list_music'))

    def list_mp3(self):
        ''' Wiiz '''
        mp3 = []
        directories = []
        main_paths = []
        for root, dirs, files in os.walk(self.__data_dir):
            main_paths.append(root)
            directories.append(dirs)
            for filename in [name for name in files]:
                if not filename.endswith('.mp3'):
                    continue
                mp3.append(filename)
        return mp3

    def get_datadir(self):
        ''' Wiiz '''
        return self.__data_dir

    def get_app_version(self):
        ''' Wiiz '''
        return self.__app_version

    def get_dl_progress(self):
        ''' Wiiz '''
        return self.__progress_percent

    data_dir = property(get_datadir, None, None, "Return the data directory path")
    app_version = property(get_app_version, None, None, "Return the application version")
    progress_percent = property(get_dl_progress, None, None, "Return the progress percentil value")

if __name__ == '__main__':
    pass
