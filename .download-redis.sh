#!/bin/bash -v
function download_redis {
  DOWNLOAD_PATH=$HOME/redis/redis-$2
  curl "$1" --output "$DOWNLOAD_PATH.tar.gz"
  if [ ! -f "$DOWNLOAD_PATH" ]; then
    mkdir "$DOWNLOAD_PATH"
  fi
  tar xzvf "$DOWNLOAD_PATH.tar.gz" --strip-components 1 -C "$DOWNLOAD_PATH"
  rm "$DOWNLOAD_PATH.tar.gz"
  (cd "$DOWNLOAD_PATH"; make)

}

if [ ! -f "$HOME/redis" ]; then
  mkdir $HOME/redis
fi

download_redis http://download.redis.io/releases/redis-7.4.1.tar.gz 7.4
download_redis http://download.redis.io/releases/redis-7.2.6.tar.gz 7.2
download_redis http://download.redis.io/releases/redis-6.2.16.tar.gz 6.2
