#!/bin/bash
#
# Posts a notification (rpush) to redis list with key defined by
# 'QUEUE_NOTIFICATIONS' variable env file.
#

# ref: https://stackoverflow.com/a/4774063/3211029
PARENT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
CURRENT_PATH="${PWD}"
cd "${PARENT_PATH}"

# Eval '.env' file to read variables
ENV_PATH="$(realpath ${PARENT_PATH}/../.env)"
echo "Sourcing env file: ${ENV_PATH}"
source $ENV_PATH

# Since redis cli will run inside docker, use alias to docker host
if [ "${REDIS_HOST}" = "localhost" ]; then
    DOCKER_INTERNAL_LOCALHOST_REF=host.docker.internal
    echo "Updating REDIS_HOST value to: ${DOCKER_INTERNAL_LOCALHOST_REF}"
    REDIS_HOST=$DOCKER_INTERNAL_LOCALHOST_REF
fi

echo
echo "Pushing notification to redis list:"
echo "  > RPUSH ${QUEUE_NOTIFICATIONS} ..."
docker run -it --rm             \
    redis:7.2.0-alpine          \
    redis-cli                   \
        -h $REDIS_HOST          \
        -p $REDIS_PORT          \
        RPUSH                   \
        $QUEUE_NOTIFICATIONS    \
        "{\"title\": \"Borgmatic\", \"content\": \"Backup is complete\"}"

cd $CURRENT_PATH
