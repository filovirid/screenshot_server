FROM ubuntu:18.04
MAINTAINER Filovirid (filovirid@protonmail.com)
RUN apt-get update 
RUN apt-get install -y -f gnupg2 apt-utils 
RUN useradd -m -s /bin/bash screenshot
COPY install_dep.sh .
COPY src /home/screenshot/
RUN chmod +x install_dep.sh
RUN ["/bin/bash","-c","./install_dep.sh"]

