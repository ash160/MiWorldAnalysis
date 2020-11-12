docker ps -a
echo Enter container code
read cont_name
docker container stop $cont_name
docker rm $cont_name
docker ps -a
docker images -a
echo Enter image name
read img_name
docker rmi $img_name
docker images -a
docker volume ls
docker volume prune
