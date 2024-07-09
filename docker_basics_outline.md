# Docker Notes

## Basic Info


```sh
docker -v
docker info
```

# Container Creation
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
--detach | -d: Run in background mode

--interactive | -i: Provide input/output

--tty | -t: Provide terminal for interactive mode

-----------------------------------------------------

## Publish Exposed Port
```sh
docker run -p 8080:80 nginx
```

-p: Publish exposed port from the Docker container to the host: -p <host_port>:<container_port>

## Run Nginx and Test
```sh
docker image pull nginx:latest
docker run -p 8080:80 nginx
curl http://localhost:8080
```
## Inspect Exposed Ports
```sh
docker image inspect nginx | jq .[].Config.ExposedPorts
```
## Run Container Once and Print Ping Output in Terminal
```sh
docker run -it --name my_container1 busybox:latest ping -c 6 localhost
```
# Container States
## List Containers
```sh
docker ps --all  # or -a
docker container ls -a
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
## Create but Don't Run a Container
```sh
docker container create --name my_container2 alpine:latest
```
## SH into a Running Container
```sh
docker run -dit --name test_cont busybox:latest
docker exec -i -t test_cont sh
```
## Inspect Containers
```sh
docker container inspect test_cont
```
# Logs
## Check Logging Driver
```sh
docker info --format '{{.LoggingDriver}}'
```

## Change Logging Driver
```ssh
Run container with --log-driver or --log-opt
```
## Check Logs in Docker Folder
```sh
docker run --name test -dit alpine:latest sh -c "while true; do $(echo time) sleep 10; done"
cd /var/lib/docker/containers
ls
# If Permission Denied switch to root user: sudo -i
# cd <container_id> ls -ltr
# cat <container_id>-json.log
```
## Check Logs via Command
```sh
docker run --name test_logs -dit alpine:latest sh -c "while true; do $(echo time) sleep 10; done"
docker ps
docker logs <container_id>  # or /test_logs
docker logs <container_id> --follow  # or -f
docker logs <id> --details
# Show last 8 entries:
docker logs /test_logs --tail 8
# Show timestamps:
docker logs /test_logs -t
# Combine flags:
docker logs /test_logs -t --tail 10

# Grep:
docker logs /test_logs | grep pattern
docker logs /test_logs | grep error
```
# Images
## Pull an Image
```sh
docker image pull ubuntu:latest
```
## Pull from Different Registry
```sh
docker pull private-docker-registry.example.com/nginx
# If auth required:
docker login -u <username> -p <password> private-docker-registry.example.com/nginx
# Side effect: your password is stored as plain text in the shell history
# Deal with it by piping the password directly from the file 'docker_password'
docker login -u <username> --password-stdin private-docker-registry.example.com < docker_password
# Windows PowerShell:
Get-Content docker_password | docker login -u <username> --password-stdin private-docker-registry.example.com
```
## Show Images
```sh
docker image ls
docker image ls --all
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
## Show Digests (Control Checksum)
```sh
docker image ls --digests
docker image history d8e1f9a8436c
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
## Save Image as Tar-file
```sh
docker image pull nginx:latest
docker image ls
docker image save <id> > mynginx.tar
ls -ltr
ls -sh mynginx.tar
```
## Save Reserve Copy
```sh
docker save --output nginx.tar nginx
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
# Dockerfile
## Dockerfile Basics
Dockerfile has commands for building a container. Every line is a new layer

```sh
FROM
# Define OS for container or a base image.
FROM <image>[:<tag>] [AS <name>]
```
```sh
WORKDIR
# Working directory for all previous commands (RUN, CMD, ENTRYPOINT, and ADD). Useful for running commands in different directories.
WORKDIR /path/to/directory
# When chained, multiple WORKDIR each create a new folder within the current directory:
WORKDIR /app
WORKDIR src
WORKDIR media
# Results in /app/src/media
```
```sh
ADD and COPY
# Allows you to transfer files from host to the container.
# COPY for basic file transfer. Recommended for local file transfer over ADD.
# COPY will create the destination if it doesn't exist; the owner is the root user; files end without slashes.
ADD
#Extract files from compressed TAR or URL.

ADD/COPY <source> <destination>

# Copy single tar file but don't decompress:
COPY hugo /app/

# Copy and decompress the file:
ADD https://github.com/.../hugo.tar.gz /app/

# Change owners:
ADD/COPY --chown=<user>:<group> <source> <destination>
# Using Wildcards

ADD/COPY *.py /app/
```
```sh
RUN
#Execute any command during the build step of the container, i.e., runs ONLY when the container is being built. Creates a new layer.
RUN <command>
# Has two forms: shell and exec.

# Shell allows using variables, pipes, chains in the instruction itself:
RUN echo 'uname -rv' > $HOME/kernel-info

# In exec form:
RUN ["executable", "parameter1", "parameter2"]
# Exec is preferred if you don't have to use pipes, variables, etc.

RUN apt-get install python
```
```sh
CMD & ENTRYPOINT
#Define which command is executed when running a container.
#CMD: Default command that runs after the container is built.
#ENTRYPOINT: Entry point for the container.
#Both have exec and shell forms.
#Exec Form

CMD ["executable", "param1", "param2"]
# Default params to ENTRYPOINT:
CMD ["param1", "param2"]

ENTRYPOINT ["executable", "param1", "param2"]
#Shell Form

CMD command param1 param2
ENTRYPOINT command param1 param2
#Example
#Setting up ENTRYPOINT as curl and running it to get the weather for your location:

FROM ubuntu:latest
RUN apt-get update && apt-get install curl -y
ENTRYPOINT ["curl", "-s"]

docker build -t sathyabhat/curl .
docker run sathyabhat/curl wttr.in
```
```sh
ENV
#Env variables are persistent through container runtime.

# Only one variable can be set per line:
ENV <key> <value>
ENV LOGS_DIR="var/log"

# Multiple variables can be set:
ENV <key>=<value>
ENV APP_DIR /app/

# Explore the env:
docker inspect sathyabhat/env | jq ".[0].Config.Env"

# Change container variables at run:
docker run -it -e LOGS_DIR="/logs/" sathyabhat/env

# Another way to check variables:
printenv | grep LOGS
```
```sh
VOLUME
#Create mount point.

VOLUME /var/logs/nginx
```
```sh
EXPOSE
#What ports are 'published' on container creation. Does not publish the port. To publish the port, use docker run with the -p flag.

EXPOSE <port> [<port>/<protocol>...]
EXPOSE 80/tcp
EXPOSE 80/udp

# Map host's port 8080 to container's 80:
docker run -d -p 8080:80 sathyabhat:web
```
```sh
LABEL
#Add metadata to an image.

LABEL author="Dave": Meta data for image
LABEL description="An example Dockerfile
```
```sh
USER
UID (user ID) or GID (group ID) for running commands.
```
# Cache
Check if an Image is in Cache and Retrieve It
To prevent caching:
```sh
docker build --no-cache
```
# Build Context
Pass the contents of URL/folder to Docker daemon.
```sh
docker build https://github.com/sathyabhat/sample-repo.git#mybranch
```
# Build Context on Tag
```sh
docker build https://github.com/sathyabhat/sample-repo.git#mytag
```
# Build on Pull Request
```sh
docker build https://github.com/sathyabhat/sample-repo.git#pull/1337/head
```
# Build Context on .tar Files
Passing root / to context will pass the contents of a drive to Docker daemon.
# Dockerignore Example
```sh
*/temp*
.DS_Store
.git
```
# BuildKit
Allows you to pass secrets into layers without the secret being in the final layer.
```sh
# Switch to legacy builder:
DOCKER_BUILDKIT=0 docker build .
#Build Test Image

FROM ubuntu:latest
CMD echo Hello World!

docker build .
```
# Image Creation Optimizations
## Multilayer Dockerfile
```sh
vi Dockerfile
FROM ubuntu:latest
ENV HOME /root
LABEL ubuntu=myubuntu
ENTRYPOINT ["sleep"]
CMD ["50"]
RUN useradd -m -G root testuser
USER root
RUN apt-get update && apt-get install net-tools -y
RUN apt-get install iputils-ping -y

# Run our Dockerfile:
docker build --tag myubuntu_image .
docker images ls --digests
```
### Unoptimized Image with Multiple RUN Commands
```sh
# Fixing unoptimized image:
FROM ubuntu:latest
ENV HOME /root
LABEL ubuntu=myubuntu
ENTRYPOINT ["sleep"]
CMD ["50"]
USER root
RUN apt-get update && apt-get install net-tools -y && apt-get install iputils-ping -y && useradd -m -G root testuser

docker build --tag myubuntu_image1 .
```
