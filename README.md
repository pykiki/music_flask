# music_flask, the music downloader

### Introduction

<b>"music_flask"</b> Web application is what you need to make downloading youtube music easier!

Based on the Flask framework, it is entirely developped in Python3.

### Pre-requisites

<p>
  Python3
  pip3
  Flask
  flask_wtf
  wtforms
  youtube_dl
  ffmpeg
</p>

### Status

!! WORK IN PROGRESS !!

### TODO

- Add TLS support
- Improve music files list design
- Add audio balise to stream online
- Add a way to delete musics
- Improve and add more flash information
- Find a way to add a progress-bar
- Add youtube-dl progessinon informations too
- Add a database simplistic system to store URL:file_name downloaded
- Avoid downloading of an previously downloaded file still present in 'data'
- A an API call to [musicbrainz](https://musicbrainz.org/) to retrieve tag informations and music names + update file with it.
- Change download mechanism to be able to download in a async manner.[async-io](https://docs.python.org/3/library/asyncio.html)
- Fill up the logger class
- Add a check for the local disk available space before download. Print a warning icon when disk space is low.

### Docker

#### Build it

You can build the docker image with the bash script included:

```bash
$ cd Docker/
$ bash -c ./build-image.sh
```

#### Start it

You must run it with user flask:

<aside class="notice">
  Please pay attention to the flag <b>--rm</b>
</aside>

```bash
$ docker run -p 80:1080 -d --user flask -h musicFlask --name music_flask --rm music_flask:latest
```

If you want to manage the downloaded files on disk, you can mount the data directory into a volume
with -v option:

```bash
$ mkdir $(pwd)/musics
$ docker run -p 80:1080 -d --user flask -h musicFlask --name music_flask -v $(pwd)/musics:/home/flask/music_flask/data --rm music_flask:latest
```

#### Manage it

  - show logs
  - attach to it
  - stop it

```bash
$ docker logs -f music_flask
$ docker exec -it music_flask sh
$ docker stop music_flask
```


### Quickstart

Create a [Python virtual environnement](https://virtualenv.pypa.io/en/stable/ "Python virtualenv")

Install music_flask:

```bash
$ python3 setup.py install
```

Now run the application:

```bash
$ python3 music_flask/music_flask.py
```

### Informations

You can find youtube-dl python call options here [Python'call options](https://github.com/rg3/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312 "Options")
