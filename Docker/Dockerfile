FROM alpine:latest

LABEL Author="PyKiki" \
      maintainer="Alain Maibach <alain.maibach@gmail.com>" \
      E-mail="alain.maibach@gmail.com" \
      Version="1" \
      Vendor="amaibach Corp." \
      Description="This is a custom Alpine image for Music Flask."

ENV PYTHONPATH "$(find '/usr/lib/' -regex '.*python[0-9].*/site-packages')"

RUN apk update && apk upgrade
RUN apk add python3 curl git shadow ffmpeg
RUN useradd flask -m -d /home/flask -s /bin/sh
RUN pip3 install --upgrade pip

WORKDIR /home/flask
RUN su - flask -c 'git clone https://github.com/pykiki/music_flask.git'
WORKDIR /home/flask/music_flask/

RUN python3 setup.py install
RUN apk del curl git shadow

STOPSIGNAL SIGTERM

ENTRYPOINT ["python3", "./music_flask/music_flask.py"]
