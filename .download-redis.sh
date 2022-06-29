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

download_redis http://download.redis.io/releases/redis-7.0.2.tar.gz 7
download_redis http://download.redis.io/releases/redis-6.2.7.tar.gz 6.2
download_redis http://download.redis.io/releases/redis-6.0.9.tar.gz 6
download_redis http://download.redis.io/releases/redis-5.0.9.tar.gz 5
download_redis http://download.redis.io/releases/redis-4.0.9.tar.gz 4
download_redis http://download.redis.io/releases/redis-3.2.9.tar.gz 3.2
download_redis http://download.redis.io/releases/redis-2.8.9.tar.gz 2.8
