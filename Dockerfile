FROM ubuntu


RUN apt update &&\
	apt install -y python3-pip &&\
	apt install -y libgl1-mesa-glx &&\
	apt install -y libglib2.0-0 &&\
	apt install -y build-essential &&\
	apt install -y libpcre3-dev libssl-dev zlib1g-dev &&\
	apt install -y git &&\
	apt install -y nano

# install yolo from source
#RUN \
#cd home &&\
#git clone https://github.com/ultralytics/yolov5 &&\
#cd yolov5 &&\
#pip install -r requirements.txt




RUN pip3 install alteia
COPY YOLO/yolov5/requirements.txt /home/requirements.txt
RUN pip3 install -r /home/requirements.txt

COPY YOLO /home/YOLO/

WORKDIR /home/YOLO/
#CMD ["sleep", "1d"]
CMD ["python3", "main.py"]
