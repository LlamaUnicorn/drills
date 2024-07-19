# Volumes

Volume and bind mount
Volumes are managed by docker, they are the recommended method for storing data
Bind mounts are host's directories handled by OS. Perform worse on Mac and Windows
Volumes are stored at Source: /var/lib/docker/volumes/data/_data

# 1. Basic volume commands
```sh
docker volume create --name=<name of the volume> --label=<any extra metadata>
docker volume inspect <volume-name>
docker volume ls
docker volume prune
docker volume rm <name>
```
# 2. Using Volumes
```sh
# Create a volume
docker volume create info
docker volume inspect info
# Look for "Mountpoint": "/var/lib/docker/volumes/info/_data",
# Create a container with this volume
docker run -it --name info-container -v info:/container-info ubuntu bash
echo "This is a file created from container having kernel `uname -r`" > /container-info/docker_kernel_info.txt
# exit and remove the container
exit
docker stop info-container
docker rm info-container
# launch a new container and check the contents of the volume
docker run -it --name new-info-container -v info:/container-info ubuntu bash
cd /container-info/
ls
# docker-kernel-info.txt
cat docker_kernel_info.txt
# This is a file created from container having kernel 4.9.87-linuxkit-aufs.
```
# 3. Populate named volume with custom data
```sh
# Create a Named Volume
docker volume create my_data_volume

# Populate the Volume with Data
# Create and run a temporary container to populate the volume
docker run --rm -v my_data_volume:/container/data -v /path/to/your/local/data:/local/data busybox cp -r /local/data/* /container/data/
# --rm: Automatically removes the container when it exits.
# -v my_data_volume:/container/data: Mounts the named volume to /container/data inside the container.
# -v /path/to/your/local/data:/local/data: Mounts the host directory containing your data to /local/data inside the container.
# cp -r /local/data/* /container/data/: Copies the data from the host directory to the volume.

# Use the Volume in Your Container
docker run -it --name my_container -v my_data_volume:/container/data busybox:latest sh

```
# 3. Bind mount
```sh
# Create folder: mkdir -p /root/testing
ls
# Create container with --volume specified and check mounted folder:
docker run -it --name myalpine -v /root/testing/:/test1 alpine:latest
ls -ltr

# Write something in container test1:
cd test1
vi myfile
# This is a demo to check for data persistence in a container
cat myfile

# Check the file in host
exit
cd /root/testing/
ls -ltr
cat myfile

# Inspect mount for this container:
cd ~
docker container ls -a
docker inspect -f '{{ json .Mounts }}' <container_id>

# Remove container and check the mount
docker ps
docker container rm myalpine -f
cd /root/testing/
ls -ltr
cat myfile
```

# 
```sh

```

# Create anonymous volume
# docker run -dit --name test_vol --volume /myapp alpine:latest
# docker container ls -a
# apt update && apt install jq -y
# docker inspect -f '{{ json .Mounts }}' <container_id> | jq

# Create named volume
# docker volume create myvolume
# docker volume inspect myvolume

# Use named volume with a new container. Multiple containers can use one volume.
# docker container run -dit --name mycentos --volume myvolume:/test centos:latest

# Use mount
# docker run -dit --name mynginx --mount source=myvol2,target=/test nginx:latest
# docker ps
# docker inspect -f '{{ json .Mounts }}' <container_id> | jq
