mkdir ~/Documents/local-data
mkdir ~/Documents/local-data/pgadmin
mkdir ~/Documents/local-data/postgres
mkdir ~/Documents/local-data/postgres/postgresdatabase
mkdir ~/Documents/local-data/postgres/postgresmetabase

sh ~/Downloads/git/the-data-analyst-toolkit/docker/setup/build_local.sh
cd ~/Downloads/git/the-data-analyst-toolkit/docker/
docker-compose up -d
docker ps
sleep 15
docker ps
sleep 15
echo "finish"
exit 0
