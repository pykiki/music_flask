#!/usr/bin/env bash
set -eu -o pipefail

# Build music flask docker image

err_report() {
  if [ ${!tmpDir[@]} ] ; then
    if [ ! -z $tmpDir ]; then
      rm -rf $tmpDir/
    fi
  fi
  badimg=$(docker images | grep -Ec '^<none>' ||true)
  if [ $badimg -gt 0 ]; then
    for dimg in $(docker images | grep -E '^<none>' | awk '{print $3}'); do
      rmdkimg "$dimg"||true
    done
  fi
  printf "Cleanly exited\n"
  exit 1
}

rmdkimg() {
  local oldImageID="$1"
  rmres="$(docker rmi ${oldImageID} 2>&1||true)"
  if [ $(grep -cFi "Error response from daemon" <<< $rmres ||true) -gt 0 ]; then
    if [ $(grep -ciE " (image is being used|is using its referenced image)" <<< $rmres ||true) -gt 0 ]; then
      container="$(grep -Eio "container.*" <<< $rmres | awk '{print $2}')"
      containername="$(docker container ls -a | grep -F "${container}" | awk '{print $12}')"
      read -p "Do you want to remove the running container $containername ? [y|n](default [n]): " answer
      if [ "${answer}" == "y" ]; then
        if [ ! -z $container ]; then
          docker stop $container &>/dev/null
          docker rm $container &>/dev/null
        else
          printf "Unable to stop container $container\n"
          err_report
        fi
        printf "\n"
      else
        err_report
      fi
    else
      printf "${rmres}\n"
      err_report
    fi
  fi
}

function control_c {
  echo -en "\nWARN: Caught SIGINT; Clean up and Exit \n"
  # Ensure that all docker processes are stopped before removing the image
  sleep 1
  err_report
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
    rmdkimg "$oldImageID"||true
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
      rmdkimg "$dimg"||true
    done
  fi
  printf "Docker Image ${dockerImgName} successfully built !\n"
fi
