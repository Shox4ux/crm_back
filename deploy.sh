#!/bin/bash
set -e

echo "🚀 Deploy started at $(date)"

cd /opt/my_crm

git pull origin main

docker compose pull
docker compose build
docker compose up -d

echo "✅ Deploy finished"
