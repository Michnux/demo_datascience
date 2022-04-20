import os
import subprocess
import sys
import alteia

from AlteiaTransactions.ImportDataset import import_dataset
from AlteiaTransactions.ImportWeights import import_weights

sys.path.insert(1, './yolov5')

PATH_TO_PICS='./dataset/images/'
PATH_TO_MODELS='./yolov5/'


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

	dataset_dir = pwd+'dataset/'
	weights_dir = pwd+'weights/'

	import_dataset(project.id, mission.id, 'yolo_inference', dataset_dir)
	# import_weights(project.id, mission.id, weights_dir)

	cmd = "python3 yolov5/detect.py --weights "+weights_dir+"yolov5s.pt --source "+dataset_dir+"images --save-txt --save-conf --project "+dataset_dir # --nosave True"
	subprocess.run(cmd, shell=True)
