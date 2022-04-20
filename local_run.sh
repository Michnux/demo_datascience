
#build docker
docker build -t inference .
docker build -t training .
#run locally
docker run -it -v work_dir:/home/work_dir --env DELAIRSTACK_PROCESS_WORKDIR='/home/work_dir/' --name ifc2mesh_1 ifc2mesh #not working, local path not recognised on Win host machine
docker run -it -v C:\Users\michael.delagarde\Documents\DEV\DemoDataScience\YOLO:/home/work_dir -e DELAIRSTACK_PROCESS_WORKDIR='/home/YOLO/' --name inference_1 inference

#push to docker hub
docker build -t docker.io/michaeldelagarde/inference .
docker push docker.io/michaeldelagarde/inference:latest

#alteia credentials create --filepath docker_credentials.json --company "5c1a2567b3c575583e8a650d"