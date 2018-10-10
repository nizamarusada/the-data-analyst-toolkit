mkdir ~/Documents/local-data
mkdir ~/Documents/local-data/pgadmin
mkdir ~/Documents/local-data/postgres
mkdir ~/Documents/local-data/postgres/postgresdatabase
mkdir ~/Documents/local-data/postgres/postgresmetabase

sh /home/nizam/Downloads/git/data_analyst_kit/docker/setup/build_local.sh
cd /home/nizam/Downloads/git/data_analyst_kit/docker/
    && docker-compose up -d
sleep 2m
echo "finish"
exit 0
