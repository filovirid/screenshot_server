#!/bin/bash 
if [ $# -ne 1 ]
then
    echo "Usage: $0 <image-name>"
    echo "<image-name>: The name of the image to build"
    exit 1
fi
user_id=$(id -u)
if [ $? -ne 0 ]
then
    echo "Can't get the User ID"
    exit -1
fi
echo "FROM ubuntu:18.04" > dockerfile
echo "MAINTAINER Filovirid (filovirid@protonmail.com)" >> dockerfile
echo "RUN apt-get update" >> dockerfile
echo "RUN apt-get -y upgrade" >> dockerfile
echo "RUN apt-get install -y -f gnupg gnupg2 apt-utils" >> dockerfile
echo "RUN useradd -m -u $user_id -s /bin/bash screenshot" >> dockerfile
echo "COPY install_dep.sh ." >> dockerfile
echo "COPY src /home/screenshot/" >> dockerfile
echo "RUN chmod +x install_dep.sh" >> dockerfile
echo 'RUN ["/bin/bash","-c","./install_dep.sh"]' >> dockerfile

echo "Building docker image...."
docker build -t $1 .
