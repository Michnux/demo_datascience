import alteia
import os
import string
import pandas as pd
import json
from pathlib import Path




#uploads weight file (.pt) to the corresponding project
def export_weights(project_id, weights_path):

	#open Alteia sdk
	sdk = alteia.SDK(config_path='./config-connections.json')

	dataset = sdk.datasets.create_file_dataset(name='yolov5_weights', project=project_id, components=['yv5.pt'], dataset_format='.pt', categories=['object detection'])
	sdk.datasets.upload_file(dataset.id, component='yv5.pt', file_path=weights_path)



if __name__ == "__main__":

	sdk = alteia.SDK(config_path='./config-connections.json')
	project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]

	export_weights(project.id)
