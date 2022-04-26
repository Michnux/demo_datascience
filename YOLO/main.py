#freely inspired from https://github.com/alteia-ai/rust-detector/blob/master/detect_rust.py#L5
import json
import logging
import os
from pathlib import Path
import sys
import time
import shutil

from train import train
from run import run
# from upload_dataset import upload_dataset


LOG_FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=LOG_FORMAT)



def load_inputs(input_path):
	inputs_desc = json.load(open(input_path))
	inputs = inputs_desc.get('inputs')
	parameters = inputs_desc.get('parameters')
	return inputs, parameters


def main():

	SCRIPT_DIR = Path(__file__).parent.resolve()
	WORKING_DIR = os.getenv('DELAIRSTACK_PROCESS_WORKDIR')
	if not WORKING_DIR:
		raise KeyError('DELAIRSTACK_PROCESS_WORKDIR environment variable must be defined')
	WORKING_DIR = Path(WORKING_DIR).resolve()

	logging.debug('WORKING_DIR :')
	logging.debug(WORKING_DIR)


	logging.debug('Extracting inputs and parameters...')
	# Retrieve inputs and parameters from inputs.json
	inputs, parameters = load_inputs(WORKING_DIR / 'inputs.json')

	logging.debug('inputs :')	
	logging.debug(inputs)
	logging.debug('parameters :')	
	logging.debug(parameters)
	logging.debug('files :')
	logging.debug(os.listdir(WORKING_DIR))


	project_id = parameters.get('project')
	mission_id = parameters.get('mission')
	input_path = inputs.get('weights').get('components')[0]['path']
	shutil.copyfile(input_path, WORKING_DIR / 'input_yv5.pt')


	if 'epochs' in parameters: #this is a training
		epochs = parameters.get('epochs')
		if 'image_size' in parameters:
			image_size = parameters.get('image_size')
		else:
			image_size=640
		print(">>>>>>>>>>>>>>>>>> lauching yolov5 train ")
		train(project_id, mission_id, epochs, image_size, WORKING_DIR)

	else: #this is a run
		print(">>>>>>>>>>>>>>>>>> lauching volov5 run ")
		run(project_id, mission_id, WORKING_DIR)


	output = {
		"outputs": {
		},
		"version": "0.1"
	}
	with open(WORKING_DIR / 'outputs.json', 'w+') as f:
		json.dump(output, f)


	logging.debug('All done...')





if __name__ == "__main__":

	main()