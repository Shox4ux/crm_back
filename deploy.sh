set -e

cd /root/crm_back

git reset --hard HEAD
git clean -fd
git pull origin main

docker compose --env-file .env up -d --build crm_back
