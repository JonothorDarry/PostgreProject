#!/bin/bash

if [[ $# -ge 1 ]]
then
	vv=$1
else
	vv="posts"
fi

docker start $vv
docker cp gak.sql $vv:/
docker cp meth.sql $vv:/
sleep 1
docker exec $vv psql -U postgres -f /gak.sql 1>/dev/null
docker exec $vv psql -U postgres -f /meth.sql 1>/dev/null
