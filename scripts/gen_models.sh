#!/bin/bash
# Uses https://koxudaxi.github.io/datamodel-code-generator/ docker image
# to generate pydantic models for entities defined in openapi.yaml
#

# Current path
# ref: https://stackoverflow.com/a/4774063/3211029
HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PARENT_DIR="$(dirname "$HERE")"

OPENAPI_FILE="${PARENT_DIR}/docs/openapi.yaml"
MODELS_FILE="${PARENT_DIR}/central/api/models.py"
MODELS_DIR="$(dirname "$MODELS_FILE")"

# Verify OPENAPI_FILE exists
if [ ! -f "${OPENAPI_FILE}" ]; then
    echo "File $OPENAPI_FILE does not exist."
    exit 1
fi

# Verify MODELS_DIR exists
if [ ! -d "${MODELS_DIR}" ]; then
    echo "Directory $MODELS_DIR does not exist."
    exit 1
fi

docker run --rm                                                    \
    -v "${OPENAPI_FILE}":/mnt/openapi.yaml                         \
    -v "${PARENT_DIR}/pyproject.toml":/mnt/central/pyproject.toml  \
    -v "${PARENT_DIR}/central/api":/mnt/central/api                \
    koxudaxi/datamodel-code-generator:latest                       \
        --capitalize-enum-members                                  \
        --input /mnt/openapi.yaml                                  \
        --input-file-type openapi                                  \
        --output-model-type pydantic_v2.BaseModel                  \
        --output /mnt/central/api/models.py


# Alternatively you can install the codegen locally
# with pip install datamodel-code-generator and use below command
# to generate pydantic models
#datamodel-codegen --input "${OPENAPI_FILE}" --output "${MODELS_FILE}"
