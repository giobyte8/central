#!/bin/bash
# Builds and optionally pushes a new version of central-web docker image
set -e

# Scripts path
# ref: https://stackoverflow.com/a/4774063/3211029
HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
BUILD_SCRIPT="build_image.sh"
DOCKERFILE="web.dockerfile"

# Use absolute paths in case that script is executed from other path
if [ ! -f "$BUILD_SCRIPT" ]; then
    BUILD_SCRIPT="${HERE}/${BUILD_SCRIPT}"
    DOCKERFILE="${HERE}/${DOCKERFILE}"
fi

IMAGE_NAME=giobyte8/central-web
IMAGE_TAG=dev
PUSH_IMAGE=false

function usage {
  echo "Usage: $0 [-t tag] [-p]"
  echo "  -h        Display this help message"
  echo "  -t tag    Tag of the image to build"
  echo "            Default tag: dev"
  echo "  -p        Push the image after building"
}

# Parse arguments and options regardless its position
# Ref: https://stackoverflow.com/a/63421397/3211029
args=()
while [ $OPTIND -le "$#" ]
do
  if getopts "tph" flag
  then
    case $flag in
      h)
        usage
        exit 0
        ;;
      t)
        IMAGE_TAG="$OPTARG"
        ;;
      p)
        PUSH_IMAGE=true
        ;;
    esac
  else
    args+=("${!OPTIND}")
    ((OPTIND++))
  fi
done

# Build image by invoking .build_image.sh script
if [ "$PUSH_IMAGE" = true ]; then
  . "$BUILD_SCRIPT" -p "$IMAGE_NAME" "$IMAGE_TAG" "$DOCKERFILE"
else
  . "$BUILD_SCRIPT" "$IMAGE_NAME" "$IMAGE_TAG" "$DOCKERFILE"
fi
