# eSteem Image Proxy

### Docker container setup

> apt install docker.io

> sudo systemctl enable docker

### Clone

> cd ~

> git clone https://github.com/esteemapp/image-proxy

> cd image-proxy

### Docker container setup

> docker network create --subnet=172.18.0.0/16 mynet

> docker build . -t image-proxy -f Dockerfile --no-cache

> docker run --net mynet --ip 172.18.0.2 --restart=always -t image-proxy