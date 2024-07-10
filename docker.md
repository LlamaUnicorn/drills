# Create
## 
## Create but Don't Run a Container
```sh
docker container create --name my_container2 alpine:latest
```
## Pull an Image
```sh
docker image pull ubuntu:latest
```
## Tag Image
Tag is a unique identifier of an image. It's recommended not to use the default 'latest' tag.
```sh
docker tag <image_id> <tag_name>
docker tag f2bafcc sathyabhat/hello-world
docker build -t sathyabhat/hello-world .
```
## Remove Image
```sh
docker rmi <image_id>
# You can't remove an image that is being used by another container. Remove the container before removing the image.
```
## Create and Save Image via Commit without Dockerfile
```sh
docker run -dit --name ubuntu ubuntu:latest
docker exec -it ubuntu sh
ping google.com
# >>> sh: 1: ping: not found
apt update && apt install iputils-ping -y
# Now it will work: ping google.com
# Save the installed 'ping' to our myubuntu image
exit
docker commit <container_name> <new_image_name>
docker commit ubuntu myubuntu

# Check available images:
docker images
# Run the new container from created image:
docker run -it --name myubuntu myubuntu sh
```
# Run test cases
## Run First Container
```sh
docker run --name my_first_container busybox:latest
```
## Run Detached, Interactive, TTY Container
```sh
docker run --detach --interactive --tty --name alpine alpine:latest
```
### Shortened:
```sh
docker run -dit --name alpine alpine:latest
```
## Pause/Unpause/Stop/Kill/Remove Container
```sh
docker run -dit --name my_container busybox:latest
docker container pause my_container
docker container unpause my_container
docker container stop my_container
docker container kill <container_id>
docker rm <container_id>
```
## Run Container Once and Print Ping Output in Terminal
```sh
docker run -it --name my_container1 busybox:latest ping -c 6 localhost
```
## Run Nginx and Test
```sh
docker image pull nginx:latest
docker run -p 8080:80 nginx
curl http://localhost:8080
```
## SH into a Running Container
```sh
docker run -dit --name test_cont busybox:latest
docker exec -i -t test_cont sh
```
# Inspect
```sh
docker -v
docker info
```
## List Containers
```sh
docker ps --all  # or -a
docker container ls -a
```
## Inspect Exposed Ports
```sh
docker image inspect nginx | jq .[].Config.ExposedPorts
```
## Inspect Containers
```sh
docker container inspect test_cont
```
## Show Images
```sh
docker image ls
docker image ls --all
```
## Inspect Image
Useful info: Env, Cmd, Layers
```sh
docker image ls
# Inspect ENV:
docker image inspect <id>|<container_name>
# Inspect CMD:
docker image inspect hello-world | jq .[].Config.Cmd
# Inspect Layers:
docker image inspect hello-world | jq .[].RootFS.Layers
```

