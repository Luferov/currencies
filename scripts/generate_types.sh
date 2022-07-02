#!/bin/bash

cd "${0%/*}"

cd ../server
python manage.py generateschema --format openapi-json --file ../client/schema.json

cd ../client
yarn run generate-types