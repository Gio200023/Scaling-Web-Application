#!/usr/bin/env bash

# choose a base image
container=$(buildah from alpine)

# choose the working directory
buildah config --env GOPATH=/root/buildah $container

# install the required packages
buildah run $container -- apk update
buildah run $container -- apk add python3

# config for 
buildah config --cmd "" $container
buildah config --entrypoint "python3 -m http.server 8000 --directory /tmp" $container

# commit to image
buildah commit $container testcontainer

# run everything with: (rm will remove the container after it exits) (-v share a directory)
# podman run --rm --name mycontainer -v /srv/objects:/objects testcontainer


