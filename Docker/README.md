Music Flask in Docker
=====================

## Build only

Just exec `$(pwd)/build-image.sh` script.

Or `docker-compose build --compress --force-rm --no-cache --pull --rm --squash`.

## Build and start

```bash
$ docker-compose -f ./docker-compose.yaml up -d --force-recreate --build --remove-orphans
```

## Clean

```bash
$ for nonimg in $(docker images | grep -F "<none>" | awk '{print $3}') ; do docker rmi $nonimg; done
```
