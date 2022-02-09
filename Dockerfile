FROM ubuntu:18.04

# Install dependencies
RUN apt-get update
RUN apt-get install -y --fix-missing python3-pip curl git wget
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN git clone --single-branch --branch v19.19 https://github.com/davisking/dlib.git
RUN cd dlib && python3 setup.py install

RUN pip3 install face_recognition flask

# Copy Data
COPY ./data /root/face_rec/

# Start Webserver
WORKDIR /root/face_rec/
CMD python3 facerec_webserver.py
