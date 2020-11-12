REDIS_BRIG = redis_bridge
POSTGRAS_BRIG = postgres_bridge 
CASSANDRA_BIG = cassandra_bridge
INTRA_TUNNEL = miworld_net
PUBLIC_TUNNEL = miworld_service 


compile:
	docker build -t --rm=true ${IMAGE_NAME} ./${DIR_NAME}

run: 
	docker run --rm --name ${CONTAINER_NAME} ${IMAGE_NAME}

net_connect:
	docker network connect --ip ${IP_ADDRESS} ${INTERFACE} ${CONTAINER_NAME}


