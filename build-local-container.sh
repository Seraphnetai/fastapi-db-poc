#!/bin/bash

docker build --ssh default --target local-development -t articles-tags .
docker compose -f docker-compose-build.yml up
