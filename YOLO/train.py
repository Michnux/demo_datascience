import os
import subprocess
import yaml
import json
from pathlib import Path
import shutil
import alteia
from AlteiaTransactions.ImportDataset import import_dataset
from AlteiaTransactions.ExportWeights import export_weights



import sys
sys.path.insert(1, './yolov5/')


def create_dataset(project_id, mission_id, WORKING_DIR):

	classes = import_dataset(project_id, mission_id, 'yolo_training', WORKING_DIR / 'dataset')

	print('classes of dataset')
	print(classes)


	#generate yaml
	yamld = {	
				'path' : str(WORKING_DIR / 'dataset'),
				'train': 'images',
				'val': 'images',
				#number of classes
				'nc': len(classes),
				#class names
				'names': classes
			}

	#dump yaml
	file_name = WORKING_DIR /'dataset/ds.yaml'

	with open(file_name, 'w') as file:
		yaml.dump(yamld, file, default_flow_style=None)





def train(project_id, mission_id, epochs, image_size, WORKING_DIR):

	create_dataset(project_id, mission_id, WORKING_DIR)

	dataset_path = WORKING_DIR / 'dataset' / 'ds.yaml'
	project_path = WORKING_DIR / 'project'
	weights_path = WORKING_DIR / 'input_yv5.pt'

	cmd = "python3 ./yolov5/train.py --img "+str(image_size)+\
									" --batch 2 --epochs "+str(epochs)+\
									" --data "+str(dataset_path)+\
									" --weights "+str(weights_path)+\
									" --project "+str(project_path)+\
									" --name current --exist-ok"  # --nosave True"
	subprocess.run(cmd, shell=True)

	# rename and copy model file to cur directory
	shutil.copyfile(project_path/'current/weights/last.pt', WORKING_DIR/'yv5.pt')

	export_weights(project_id, WORKING_DIR/'yv5.pt')






if __name__ == "__main__":

	sdk = alteia.SDK(config_path='./config-connections.json')
	project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]
	mission = sdk.missions.search(filter={'project': {'$eq': project.id}})[0]
	
	epochs = 10
	WORKING_DIR = Path('./').resolve()

	train(project.id, mission.id, epochs, WORKING_DIR)