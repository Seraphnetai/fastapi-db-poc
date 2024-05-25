#!/bin/bash

docker build --ssh default --target local-development -t fastapi-template .
docker compose -f docker-compose-build.yml up
