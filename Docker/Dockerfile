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
RUN pip3 install Flask wtforms flask_wtf

RUN mkdir -p \$PYTHONPATH/wheel/youtube_dl/
WORKDIR $PYTHONPATH/wheel/youtube_dl/
RUN curl -L "https://files.pythonhosted.org/packages/38/98/759cc271d2cda665671a835689b3fb5c5dcd6a3a3cdaf81164dd270cb263/youtube_dl-2018.4.16-py2.py3-none-any.whl" -O
RUN pip3 install youtube_dl
# send error logs and start logs to docker logs
#RUN ln -sf /proc/self/fd/1 /var/log/error.log

STOPSIGNAL SIGTERM

WORKDIR /home/flask
RUN su - flask -c 'git clone https://github.com/pykiki/music_flask.git'
WORKDIR /home/flask/music_flask/
#RUN su - flask -c 'mkdir /home/flask/music_flask/data'
RUN apk del curl git shadow

ENTRYPOINT ["python3", "./music_flask.py"]
