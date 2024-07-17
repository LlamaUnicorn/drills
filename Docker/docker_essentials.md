# 1. Run nginx and test if it runs
```sh
docker image pull nginx:latest
docker run --name my-testing-nginx -p 8080:80 nginx
curl http://localhost:8080
```
# 2. Stop a container
```sh
docker container stop my_container
```
# 3. Remove a container
```sh
docker ps -a
docker rm <container_id>
```
# 4. Remove image
```sh
docker rmi <image_id>
docker image prune
```

# 5. Run container once and print ping output in terminal
```sh
docker run -it --name my_sh_container busybox:latest ping -c 6 localhost
```


# 6. Container states
Kill a container that's not stopping
Remove a container
Create but don't run a container
```sh
docker run -dit --name my_container busybox:latest
# to start a container: docker start container-name
docker container pause my_container
docker container unpause my_container
docker container stop my_container
docker ps -a
docker container kill <container_id>
docker rm <container_id>
docker container create --name my_container2 alpine:latest
```
# 7. SH into a running container
```sh
docker run -dit --name test_cont busybox:latest
docker exec -i -t test_cont sh
```

# 8. Inspect containers
```sh
docker container inspect test_cont
```
# 9. Check logs in docker folder
```sh
docker run --name test -dit alpine:latest sh -c "while true; do $(echo time) sleep 10; done"
cd /var/lib/docker/containers
#if Permission Denied switch to root user: sudo -i
#use 'exit' to switch back
ls
#cd <container_id> ls -ltr
#cat <container_id>-json.log
```
# 10. Check logs via command
```sh
docker run --name test_logs -dit alpine:latest sh -c "while true; do $(echo time) sleep 10; done"
docker ps
docker logs <container_id> or /test_logs
docker logs <container_id> --follow | -f
docker logs <id> --details
#show last 8 entries: docker logs /test_logs --tail 8
#show timestamps: docker logs /test_logs -t
#combine flags: docker logs /test_logs -t --tail 10
grep: docker logs /test_logs | grep pattern
docker logs /test_logs | grep error
```
# 11. Pull an image
```sh
docker image pull ubuntu:latest
```
# 12. Show images
```sh
docker images
docker image ls
docker image ls | --all
```
# 13. Tag image
```sh
docker tag <image_id> <tag_name>
docker tag f2bafcc sathyabhat/hello-world
docker build -t sathyabhat/hello-world .
```
# 14. Remove image
```sh
docker rmi <image_id>
#You can't remove image that is being used by another container. Remove the container before removing the image.
```
# 15. Create and Save image via commit without the dockerfile (install ping into ubuntu image and save changed image)
```sh
docker run -dit --name ubuntu ubuntu:latest
docker exec -it ubuntu sh
ping google.com
#>>> sh: 1: ping: not found
apt update && apt install iputils-ping -y
#now it will work: ping google.com
#Save the installed 'ping' to our myubuntu image
exit
docker commit <container_name> <new_image_name>
docker commit ubuntu myubuntu
#Check available images:
docker images
#Run the new container from created image:
docker run -it --name myubuntu myubuntu sh
```
#  16. Setting up entrypoint as curl and running it to get the weather for your location
```sh
FROM ubuntu:latest
RUN apt-get update && apt-get install curl -y
ENTRYPOINT ["curl", "-s"]

docker build -t sathyabhat/curl .

docker run sathyabhat/curl wttr.in
```