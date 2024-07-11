# 1. run nginx and test if it runs
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
docker images
docker rm <container_id>
```
# 4. Remove image
```sh
docker rmi <image_id>
docker image prune
```

# 5. Run container once and print ping output in terminal
docker run -it --name my_container1 busybox:latest ping -c 6 localhost
```sh
docker run -it --name my_sh_container busybox:latest ping -c 6 localhost
```


# 
```sh

```
# 
```sh

```
