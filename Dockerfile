FROM pytorch/pytorch


RUN apt update
#RUN apt -y install python3.8
RUN apt -y install python3-pip

RUN apt install -y libgl1-mesa-glx
RUN apt install -y libglib2.0-0

RUN apt install -y build-essential
RUN apt install -y libpcre3-dev libssl-dev zlib1g-dev
RUN apt install -y git
RUN apt install -y nano

# install yolo from source
#RUN \
#cd home &&\
#git clone https://github.com/ultralytics/yolov5 &&\
#cd yolov5 &&\
#pip install -r requirements.txt




RUN pip3 install alteia
COPY YOLO/yolov5/requirements.txt /home/requirements.txt
RUN pip3 install -r /home/requirements.txt

#COPY script_dir /home/script_dir/
#COPY python /home/python/

CMD ["sleep", "1d"]
#CMD ["python3", "/home/script_dir/main.py"]
