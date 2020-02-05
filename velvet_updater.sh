docker start posts
docker cp gak.sql posts:/
docker cp meth.sql posts:/
docker exec posts psql -U postgres -f /gak.sql 1>/dev/null
docker exec posts psql -U postgres -f /meth.sql 1>/dev/null
