# music_flask, the music downloader

### Introduction

<b>"music_flask"</b> WEB application is what you need to make downloading youtube music easier !

Based on the Flask framework, it is entirely developped in Pyhton3.

### Pre-requisites

<p>
  Python3
  pip3
  Python Flask 
  youtube_dl
</p>

### Status

!! WORK IN PROGRESS !!

### TODO

- Mettre en place un moyen de conserver les URL associé au nom du fichier telecharger pour ne pas re faire le telechargement si le fichier existe dans data/
- mettre en place les rechargement auto
- les bouttons de navigation si necessaire
- ajouter l'appel a l'api musicbrainz (https://musicbrainz.org/) et renommer en fonction + ajouter les tag dans le fichier
- ajouter les balise audio pour l'ecoute en streaming
- ajouter la possibilité de supprimer les music
- ameliorer la gestion de la longueure du champs pour l'URL
- ajouter la possibilité de passer plusieurs URL
- mettre en place le telechargement en parallèle (avec async-io)
- ajouter des information de progression
- remplir la classe des logger
- ajouter la gestion de la taille disponible dans le repertoire data, ajouter l'affichage d'une alerte si espace faible.

### Quickstart

Create a [Python virtual environnement](https://virtualenv.pypa.io/en/stable/ "Python virtualenv") and then install Flask.

```bash
$ pip install Flask
```

Install [youtube_dl](https://github.com/rg3/youtube-dl/blob/master/README.md#readme "Documentation youtube_dl")
```bash
mkdir -p $PYTHONPATH/wheel/youtube_dl/
pushd $PYTHONPATH/wheel/youtube_dl/
curl -L "https://files.pythonhosted.org/packages/38/98/759cc271d2cda665671a835689b3fb5c5dcd6a3a3cdaf81164dd270cb263/youtube_dl-2018.4.16-py2.py3-none-any.whl" -O
popd
pip install youtube_dl
```

Now run the application

```bash
$ python3 ./music_flask.py
```

### Informations

You can find youtube-dl python call options here [Python'call options](https://github.com/rg3/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312 "Options")
