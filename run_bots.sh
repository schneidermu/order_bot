#!/usr/bin/env bash

git checkout main
git pull
docker compose -f docker-compose.yml down
docker compose -f docker-compose.yml up -d --build && \
docker network connect protocol_model digital_protocol_container