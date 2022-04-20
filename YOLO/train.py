import os
import yaml
import json
import alteia
from AlteiaTransactions.ImportDataset import import_dataset



import sys
sys.path.insert(1, './yolov5/')


def create_dataset(project_id, mission_id, classes, destination_folder):


	import_dataset(project_id, mission_id, 'yolo_training', destination_folder)



	#generate yaml
	yamld = {	'train': destination_folder+'images/',
				'val': destination_folder+'images/',
				#number of classes
				'nc': len(classes),
				#class names
				'names': json.dumps(classes)[1:-1]
			}

	#dump yaml
	file_name = destination_folder+'ds.yaml'

	with open(file_name, 'w') as file:
		yaml.dump(yamld, file)


	return destination_folder, file_name




if __name__ == "__main__":



	#get current folder
	pwd = os.getcwd()
	spl = pwd.split('\\')
	pwd=''
	for s in spl:
		pwd+=s+'/'


	sdk = alteia.SDK(config_path='./config-connections.json')
	project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]
	mission = sdk.missions.search(filter={'project': {'$eq': project.id}})[0]

	destination_folder = pwd+'dataset/'

	classes = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
	
	ds_dir, ds_file = create_dataset(project.id, mission.id, classes, destination_folder)

	os.system('python3 ./yolov5/train.py --img 640 --batch 16 --epochs 500 --data '+ds_file+' --weights yolov5s.pt --name current --exist-ok')


	# rename and copy model file to model directory
	# copyfile('./runs/train/current/weights/last.pt', ds_dir+'yv5.pt')
	# copyfile(ds_dir+'yv5.pt', PATH_TO_VIDS+'models/yv5.pt')