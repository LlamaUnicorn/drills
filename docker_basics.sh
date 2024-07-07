#reformat:
#Commands and flags
#Use cases/scenarios

#Basic info
docker -v
docker info

#Run first container
docker run --name my_first_container busybox:latest

docker run --detach --interactive --tty --name alpine alpine:latest
#shortened:
docker run -dit --name alpine alpine:latest
#--detach | -d - run in background mode
#--interactive | -i - provide input/output
#--tty | -t - provide terminal for interactive mode

#-p publish exposed port from the docker container to the host: -p <host_port>:<container_port>
docker run -p 8080:80 nginx

#run nginx and test if it runs
docker image pull nginx:latest
docker run -p 8080:80 nginx
curl http://localhost:8080

#inspect exposed ports
docker image inspect nginx | jq .[].Config]ExposedPorts

#Run container once and print ping output in terminal
docker run -it --name my_container1 busybox:latest ping -c 6 localhost


#Container states
# ps shows only active running containers. --all shows all containers
docker ps --all | -a
docker container ls -a

docker run -dit --name my_container busybox:latest

#Pause a container
docker container pause my_container

#Unpause a container
docker container unpause my_container

#Stop a container
docker container stop my_container

#Kill a container that's not stopping
docker container kill <container_id>

#Remove a container
docker rm <container_id>

#Create but don't run a container
docker container create --name my_container2 alpine:latest


#SH into a running container
docker run -dit --name test_cont busybox:latest
docker exec -i -t test_cont sh


#Inspect containers
docker container inspect test_cont

#Logs
#Check logging driver
docker info --format '{{.LoggingDriver}}'

#Change logging driver:
run container with --log-driver or --log-opt

#Check logs in docker folder
docker run --name test -dit alpine:latest sh -c "while true; do $(echo time) sleep 10; done"
cd /var/lib/docker/containers
#if Permission Denied switch to root user: sudo -i
#use 'exit' to switch back
ls
#cd <container_id> ls -ltr
#cat <container_id>-json.log


#Check logs via command
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


#Images
#pull an image:
docker image pull ubuntu:latest
#pull from different registry, not docker hub
docker pull private-docker-registry.example.com/nginx
#if auth required
docker login -u <username> -p <password> private-docker-registry.example.com/nginx

#side effect: your password is stored as plain text in the shell history
#you can deal with it by piping the password directly from the file 'docker_password' with your password
docker login -u <username> --password-stdin private-docker-registry.example.com < docker_password
#windows powershell:
Get-Content docker_password | docker login -u <username> --password-stdin private-docker-registry.example.com

#Show images
docker image ls
docker image ls | --all

#Tag is a unique identifier of an image. It is Recommended not to use default 'latest' tag 
# since it overwrites previous versions and it's harder to rollback to a stable version.
#Tag image
docker tag <image_id> <tag_name>
docker tag f2bafcc sathyabhat/hello-world
docker build -t sathyabhat/hello-world .

#Remove image
docker rmi <image_id>
#You can't remove image that is being used by another container. Remove the container before removing the image.

#show digests (control checksum):
docker image ls --digests
docker image history d8e1f9a8436c

#docker info
#look for Storage Driver: overlay2
#Check images:
sudo -i
cd /var/lib/docker/overlay2
ls -ltr

#Inspect image
#Useful info: Env, Cmd, Layers
docker image ls
#docker image inspect <id>|<container_name>
#Inspect ENV: docker image inspect hello-world | jq .[].Config.Env
#Inspect CMD: docker image inspect hello-world | jq .[].Config.Cmd
#Inspect Layers: docker image inspect hello-world | jq .[].RootFS.Layers

#Save image as tar-file
docker image pull nginx:latest
docker image ls
docker image save <id> > mynginx.tar
ls -ltr
ls -sh mynginx.tar

#Save reserve copy:
docker save --output nginx.tar nginx


#Create and Save image via commit without the dockerfile (install ping into ubuntu image and save changed image)
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



#Dockerfile
#Dockerfile has commands for building a container
#Every line is a new layer
FROM: define OS for container or a base image.
FROM <image>[:<tag>] [AS <name>]

WORKDIR: working directory for all previous commands (RUN, CMD, ENTRYPOINT and ADD). Useful for running commands in different directories
WORKDIR: /path/to/directory
When chained multiple WORKDIR they each create a new folder within current directory
WORKDIR: /app
WORKDIR: src
WORKDIR: media
results in /app/src/media

ADD and COPY

Allows you to transfer files from host to the container.
COPY for basic files transfer. Recommended for local file transfer over ADD.
COPY will create destination if it doesnt exist; owner is the root user; files end without slashes

ADD extract files from compressed TAR or URL
ADD/COPY <source> <destination>

Copy single tar file but don\'t decompress:
COPY hugo /app/

Copy and decompress the file
ADD https://github.com/.../hugo.tar.gz /app/

Change owners
ADD/COPY --chown=<user>:<group> <source> <destination>

ADD/COPY requirements.txt /usr/share/app

Using wildcards:
ADD/COPY *.py /app/

RUN
RUN will execute any command during the build step of the container, i.e. runs ONLY when the container is being built. Creates a new layer.
RUN <command>

Has two forms: shell and exec.

Shell allows using variables, pipes, chains in the instruction itself
Embed kernel info into the home directory:
RUN echo 'uname -rv' > $HOME/kernel-info

In exec form:
RUN ["executible", "parameter1", "parameter2"]
Exec is preferred if you dont have to use pipes, variables, etc.

RUN: apt-get install python


CMD & ENTRYPOINT define which command is executed when running a container.
CMD: default command that runs after the container is built
ENTRYPOINT: entry point for the rontainer. 
You can specify the entrypoint as executable with a param and run the container.

Both have exec and shell forms. 

Exec:

CMD ["executable", "param1", "param2"]

Default params to ENTRYPOINT:
CMD ["param1", "param2"]

ENTRYPOINT ["executable", "param1", "param2"]

Shell:
CMD command param1 param2

ENTRYPOINT command param1 param2

Example of setting up entrypoint as curl and running it to get the weather for your location:

The ENTRYPOINT in your Dockerfile is set to ["curl", "-s"]. This means that any arguments you pass to docker run will be appended to curl -s
This will work only when ENTRYPOINT is in the exec mode: 
ENTRYPOINT ["executable", "param1", "param2"]

FROM ubuntu:latest
RUN apt-get update && apt-get install curl -y
ENTRYPOINT ["curl", "-s"]

docker build -t sathyabhat/curl .

docker run sathyabhat/curl wttr.in


ENV: env variables are persistent through container runtime.

Only one variable can be set per line:
ENV <key> <value>
ENV LOGS_DIR="var/log"

Multiple variables can be set:
ENV <key>=<value>
ENV APP_DIR /app/

Explore the env:
docker inspect sathyabhat/env | jq ".[0].Config.Env"

Change container variables at run:
docker run -it -e LOGS_DIR="/logs/" sathyabhat/env

Another way to check variables:
printenv | grep LOGS


VOLUME: create mount point
VOLUME /var/logs/nginx


EXPOSE: what ports are 'published' on container creation. Does not publish the port. To publish the port use docker run with -p flag.
EXPOSE <port> [<port>/<protocol>...]
EXPOSE 80/tcp
EXPOSE 80/udp

Map hosts port 8080 to containers 80
docker run -d -p 8080:80 sathyabhat:web


LABEL add metadata to an image
LABEL author="Dave": Meta data for image
LABEL description="An example Dockerfile"



USER: UID (user ID) or GID (group ID) for running commands

#Cache
#Check if an image is in cache and retrieve it
#To prevent caching use 
docker build --no-cache 

#Build context. Pass the contents of URL/folder to docker daemon
docker build https://github.com/sathyabhat/sample-repo.git#mybranch

#Build context on tag
docker build https://github.com/sathyabhat/sample-repo.git#mytag

#Build on pull request
docker build https://github.com/sathyabhat/sample-repo.git#pull/1337/head

#You can build context on .tar files
#Passing root / to context will pass the contents of a drive to docker daemon

#Dockerignore example
*/temp*
.DS_Store
.git

#BuildKit allows you to pass secrets into layers without the secret being in the final layer.
#Switch to legacy builder
DOCKER_BUILDKIT=0 docker build .

#Build test image
FROM ubuntu:latest
CMD echo Hello World!

docker build .


#Image creation optimizations
#Multilayer dockerfile
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

#Run our Dockerfile
docker build --tag myubuntu_image .

docker images ls --digests

#We've created unoptimized image containing multiple RUN commands. Let's fix that.
# RUN ADD COPY create layers
FROM ubuntu:latest
ENV HOME /root
LABEL ubuntu=myubuntu
ENTRYPOINT ["sleep"]
CMD ["50"]
USER root
RUN apt-get update && apt-get install net-tools -y && apt-get install iputils-ping -y && useradd -m -G root testuser

docker build --tag myubuntu_image1 .



Multistage builds
When you need build time dependencies but they are not needed during runtime.
Build layers are used to build the image. Final image is used to run container.
