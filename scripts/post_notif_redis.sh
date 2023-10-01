#!/bin/bash
#
# Posts a notification (rpush) to redis list with key defined by
# 'QUEUE_NOTIFICATIONS' variable env file.
#

# ref: https://stackoverflow.com/a/4774063/3211029
PARENT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
CURRENT_PATH="${PWD}"

# Eval '.env' file to read variables
cd "${PARENT_PATH}"
source ../.env

# Since redis cli will run inside docker, use alias to docker host
if [ "${REDIS_HOST}" = "localhost" ]; then
    REDIS_HOST=host.docker.internal
fi

docker run -it --rm             \
    redis:7.2.0-alpine          \
    redis-cli                   \
        -h $REDIS_HOST          \
        -p $REDIS_PORT          \
        RPUSH                   \
        $QUEUE_NOTIFICATIONS    \
        "{\"title\": \"Borgmatic\", \"content\": \"Backup is complete\"}"

cd $CURRENT_PATH
