#
# Ubuntu Dockerfile
#
# https://github.com/dockerfile/ubuntu
#

# Pull base image.
FROM ubuntu

ENV http_proxy http://proxy.ubisoft.org:3128
ENV https_proxy https://proxy.ubisoft.org:3128

# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  apt-get install -y alsa alsa-tools && \
  apt-get install -y  python3-pip && \
  rm -rf /var/lib/apt/lists/*

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /usr/src/app

ENV http_proxy http://proxy.ubisoft.org:3128
ENV https_proxy https://proxy.ubisoft.org:3128

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "./record.py" ]
CMD [ "bash"]
