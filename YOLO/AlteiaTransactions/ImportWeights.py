import alteia
import os
import string
import pandas as pd




def import_weights(project_id, mission_id, destination_folder):

	#create destination dir if doesn't exist
	if not os.path.isdir(destination_folder):
		os.mkdir(destination_folder)

	#open Alteia sdk
	sdk = alteia.SDK(config_path='./config-connections.json')

	#get images datasets of specified project and mission
	datasets = sdk.datasets.search(filter={'project': {'$eq': project_id}})
	weights_datasets = [d for d in datasets if d.format=='pt']
	sdk.datasets.download_component(weights_datasets[0].id, component=weights_datasets[0].components[0]['name'], target_path=destination_folder, target_name='yolov5.pt')




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

	destination_folder = pwd+'weights/'

	import_weights(project.id, mission.id, destination_folder)