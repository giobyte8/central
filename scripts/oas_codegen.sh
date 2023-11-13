# Current path
# ref: https://stackoverflow.com/a/4774063/3211029
HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

docker run --rm                                         \
    -v "${HERE}/codegen":/mnt/codegen                   \
    -v "${HERE}/../docs/openapi.yaml:/mnt/openapi.yaml" \
    openapitools/openapi-generator-cli generate         \
      -i /mnt/openapi.yaml                              \
      -g python-aiohttp                                         \
      -o /mnt/codegen/