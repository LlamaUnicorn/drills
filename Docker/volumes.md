# Volumes

# Check current storage driver
# docker info | grep Storage

# Change driver from overlay2 to overlay
# Stop docker: systemctl docker stop
# Copy to another location:
# cp -au /var/lib/docker /var/docker.bkp
# Change daemon.json:
# {
# "storage-driver": "overlay"
# }
# Start docker: systemctl start docker
# Check the driver: docker info | grep Storage

# Volume and bind mount
# Volume are managed by docker, they are recommended method for storing data
# Bind mounts are host's directories handled by OS. Perform worse on Mac and Windows

# Bind mount
# Create folder: mkdir -p /root/testing
# ls

# Create container with --volume specified and check mounted folder:
# docker run -it --name myalpine -v /root/testing/:/test1 alpine:latest
# ls -ltr

# Write something in container's test1:
# cd test1
# vi myfile
# This is a demo to check for data persistence in a container
# cat myfile

# Check the file in host
# exit
# cd /root/testing/
# ls -ltr
# cat myfile

# Inspect mount for this container:
# cd ~
# docker container ls -a
# docker inspect -f '{{ json .Mounts }}' <container_id>

# Remove container and check the mount
# docker ps
# docker container rm myalpine -f
# cd /root/testing/
# ls -ltr
# cat myfile

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
