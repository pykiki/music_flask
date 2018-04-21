#!/usr/bin/env bash
set -eu -o pipefail

# Build music flask docker image

err_report() {
  if [ ! -z $tmpDir ]; then
    rm -rf $tmpDir/
  fi
  badimg=$(docker images | grep -Ec '^<none>' ||true)
  if [ $badimg -gt 0 ]; then
    for dimg in $(docker images | grep -E '^<none>' | awk '{print $3}'); do
      docker rmi $dimg
    done
  fi
}

function control_c {
  echo -en "\nWARN: Caught SIGINT; Clean up and Exit \n"
  # Ensure that all docker processes are stopped before removing the image
  sleep 1
  rm -rf $tmpDir/
  badimg=$(docker images | grep -Ec '^<none>' ||true)
  if [ $badimg -gt 0 ]; then
    for dimg in $(docker images | grep -E '^<none>' | awk '{print $3}'); do
      docker rmi $dimg
    done
  fi
  exit $?
}

trap "err_report \"Line number ${LINENO} failed: $BASH_COMMAND.\"" ERR
trap control_c SIGINT
trap control_c SIGTERM

# Main()

dockerImgName="music_flask"

imgfound=$(docker images | grep -Ec "^${dockerImgName} [[:space:]].*$" 2>&1 ||true)
if [ $imgfound -gt 0 ]; then
  oldImageID="$(docker images | grep -i "${dockerImgName}" | awk -F' ' '{print $3}')"
  if [ "$oldImageID" != "" ]; then
      printf "Cleaning current Docker image: $oldImageID / ${dockerImgName}\n"
      docker rmi ${oldImageID} 2>&1 > /dev/null
  fi
fi

tmpDir="$(mktemp -d)"
workDir="$(pwd)"

install ./Dockerfile ${tmpDir}/Dockerfile

pushd $tmpDir/
printf "Building docker image ${dockerImgName}\n"
# we are using --squash because we want to replace the image for every build.
docker build --compress --no-cache=true --rm -f $tmpDir/Dockerfile --tag ${dockerImgName}:latest --force-rm --squash $tmpDir/

unset imgfound
imgfound=$(docker images | grep -Ec "^${dockerImgName} [[:space:]].*$" 2>&1 ||true)
if [ $imgfound -gt 0 ]; then
  rm -rf $tmpDir/
  badimg=$(docker images | grep -Ec '^<none>' ||true)
  if [ $badimg -gt 0 ]; then
    for dimg in $(docker images | grep -E '^<none>' | awk '{print $3}'); do
      docker rmi $dimg
    done
  fi
  printf "Docker Image ${dockerImgName} successfully built !\n"
fi
