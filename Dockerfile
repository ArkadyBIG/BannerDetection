FROM mathieudu/gstreamer-auteur
RUN apt update 
RUN apt-get install -y  git 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
RUN apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
RUN apt-get install -y htop
RUN python3 -m pip install numpy streamlink imutils tqdm matplotlib
WORKDIR  /
RUN git clone https://github.com/opencv/opencv 


RUN mkdir release
WORKDIR /opencv/release 

RUN ls ..
RUN apt-get install -y  python3-dev 
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D PYTHON_EXECUTABLE=/usr/bin/python3 \
-D BUILD_opencv_python2=OFF \
-D CMAKE_INSTALL_PREFIX=/usr \
-D PYTHON3_EXECUTABLE=/usr/bin/python3 \
-D PYTHON3_INCLUDE_DIR=/usr/include/python3.8 \
-D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
-D WITH_GSTREAMER=ON \
-D WITH_FFMPEG=OFF \
-D BUILD_EXAMPLES=ON ..

RUN make

RUN make install

RUN mkdir /workspace
COPY . /workspace
WORKDIR /workspace
