#!/bin/bash

docker create --name kyxsetup -it abz
docker start kyxsetup
docker exec -it kyxsetup wolframscript "-activate"
docker exec kyxsetup java -jar keymaerax-webui-5.1.1.jar setup --tool WolframEngine
docker stop kyxsetup
docker commit kyxsetup kyxabz:activated
