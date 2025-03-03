# How to run

The docker image can be built directly or downloaded online.

## Building the image (Option 1)

Go in docker/ and run
`docker build -t abz .`

## Downloading the image (Option 2)

The image (x86) can be accessed on github and downloaded like so:
```
docker pull ghcr.io/ls-lab/drl-abz25
docker tag ghcr.io/ls-lab/drl-abz25 abz
```

## Setting up

First run `docker/docker-setup.sh`
This require the wolfram engine free licence.
[https://wolfram.com/developer-license](https://wolfram.com/developer-license)

## KeYmaera X proofs

All KeYmaera X proofs can be ran by `docker/docker-proofs.sh`

## Versaille verification

The verification of the neural network can be done by `docker/docker-nnv.sh`

Caution: verification may **last several hours**

### Analysis of results
By default, docker saves the verification results inside the Docker container.
To move the files to the host, [you need to copy them while the container is still running](https://stackoverflow.com/questions/22049212/copying-files-from-docker-container-to-host).

The repository also contains the previous verification results.  
These can be inspected as explained [here](versaille/README.md)