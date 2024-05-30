#-------------------------------------------------------
# cuda=11.3, cudnn=8, tensorflow=2.8.0 protobuf=3.20.3
# test env1: i9 10900x, rtx3090ti
#-------------------------------------------------------
#FROM tensorflow/tensorflow:2.5.1-gpu
#FROM nvidia/cuda:11.2.0-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

RUN sed -i 's@archive.ubuntu.com@ftp.jaist.ac.jp/pub/Linux@g' /etc/apt/sources.list

#---------------------------------------------
# environment variables
#---------------------------------------------
ENV DEBIAN_FRONTEND noninteractive

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV LC_ALL=C.UTF-8
ENV export LANG=C.UTF-8

ENV SHELL /bin/bash

#---------------------------------------------
# apt, pip install
#---------------------------------------------
RUN apt update -y; apt install -y \
lsb-release \
git \
vim \
cmake \
libsm6 \
libxext6 \
libxrender-dev \
python3 \
python3-pip  \
curl \
gnupg2

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install --upgrade pip 
RUN pip3 install rospkg

#-------------------------------
# install tensorflow with gpu
#-------------------------------
RUN python3 -m pip install tensorflow==2.8.0
RUN pip3 install protobuf==3.20.3

#-------------------------------
# install deep face, retinaface
#-------------------------------
#RUN pip3 install tensorflow==2.5.0
#RUN pip3 install tensorflow==2.5.1
#RUN pip3 install torch==1.8.1 torchvision==0.9.1 torchaudio==0.8.1
RUN pip3 install deepface
RUN pip3 install retina-face

#-----------------------------
# solution for cuda nopub key
#-----------------------------
#COPY ./cuda-keyring_1.0-1_all.deb cuda-keyring_1.0-1_all.deb
#RUN apt-key del 7fa2af80

#RUN apt install -y wget
#RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
#
#RUN rm /etc/apt/sources.list.d/cuda.list && \
#    rm /etc/apt/sources.list.d/nvidia-ml.list && \
#    dpkg -i cuda-keyring_1.0-1_all.deb
#
#RUN apt-get -y update

#-----------------------------
# intall ros-noetic
#-----------------------------
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' \
    && curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt update

RUN apt-get update && apt-get install -y \
    ros-noetic-desktop-full

#-----------------------------
# create catkin_ws
#-----------------------------
WORKDIR catkin_ws
RUN echo "source /opt/ros/noetic/setup.sh" >> .bashrc
RUN mkdir src
COPY ./face_recognizer /catkin_ws/src/face_recognizer
RUN cd /catkin_ws/src && /bin/bash -c '. /opt/ros/noetic/setup.bash; catkin_init_workspace'
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; cd /catkin_ws; catkin_make'

#solution for import error libGL.so.1
RUN apt -y install libopencv-dev 

RUN pip install face_recognition


COPY ./ros_entrypoint.sh /
ENTRYPOINT ["/ros_entrypoint.sh"]
