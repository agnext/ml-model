# FROM tensorflow/serving:2.8.0-gpu
FROM tensorflow/serving:1.14.0-gpu
#FROM tensorflow/serving:latest-gpu

#------------------------------------------------------
#apt stuff
#------------------------------------------------------
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing
RUN apt-get install -y vim net-tools htop


RUN mkdir -p /tf_files/agshift

COPY . /tf_files/agshift/ml-models/

COPY config/models.conf /models/models.config
# docker build -t tf-serving-docker-1.14 .
