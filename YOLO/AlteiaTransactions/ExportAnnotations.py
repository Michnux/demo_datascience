import alteia
import os
import string
import pandas as pd
import json
from pathlib import Path
from matplotlib import cm



annotations_formats = ['SuperAnnotate', 'yolo']


#takes annotations and uploads them as alteia annotations on the corresponding pictures
def export_annotations(project_id, mission_id, annotations_format, annotations_dir):

	#open Alteia sdk
	sdk = alteia.SDK(config_path='./config-connections.json')

	#get images datasets of specified project and mission
	datasets = sdk.datasets.search(filter={'project': {'$eq': project_id}, 'mission': {'$eq': mission_id}})
	images_datasets = [d for d in datasets if d.type=='image']

	df_images = pd.DataFrame()

	for d in images_datasets:
		df_images = pd.concat([df_images, pd.DataFrame({
							'image_name':[d.name],
							'image_id':[d.id],
							'size_x':[d.width],
							'size_y':[d.height]
						})])

	df_images=df_images.drop_duplicates() #it is assumed there is no duplicates

	print(df_images.to_string())

	#put yolo annotations in a pandas df
	if annotations_format=='yolo':

		an_files=os.listdir(annotations_dir/'labels/')
		df_annotations = pd.DataFrame(columns = ['class', 'x', 'y', 'width', 'height', 'score', 'image_name'])

		for f in an_files:
			# df = pd.read_csv(annotations_dir/'labels'/f, sep=' ', names=['class', 'x', 'y', 'width', 'height', 'score'], header=None, index_col=False)
			df = pd.read_csv(annotations_dir/'labels'/f, sep=' ', names=['class', 'x', 'y', 'width', 'height'], header=None, index_col=False)
			df['image_name']=f[:-4]
			df_annotations = pd.concat([df_annotations, df])


		df_annotations = df_annotations.join(df_images.set_index('image_name')[['image_id','size_x','size_y']], on='image_name')

		df_annotations['x1']=(df_annotations['x']-df_annotations['width']/2)*df_annotations['size_x']
		df_annotations['x2']=(df_annotations['x']+df_annotations['width']/2)*df_annotations['size_x']
		df_annotations['y1']=df_annotations['size_y']-(df_annotations['y']-df_annotations['height']/2)*df_annotations['size_y']
		df_annotations['y2']=df_annotations['size_y']-(df_annotations['y']+df_annotations['height']/2)*df_annotations['size_y']

		# df_annotations['class_name']=df_annotations['class'].map(lambda x: str(x)) #fixme

		# print(df_annotations.to_string())

		#put classes_names in exp/classes.json in a pandas dataframe (index = clss)
		with open(annotations_dir/'classes.json', 'r') as class_file:
			class_names = json.load(class_file)
			df_classes = pd.DataFrame()
			df_classes['class_name'] = class_names
		#join class_name to df_annotation (on class)
		df_annotations = df_annotations.join(df_classes, on='class')


	print(df_annotations.to_string())

	cmap_boxes = cm.get_cmap("Set1") # colour map

	#create alteia annotations
	for _, r in df_annotations.iterrows():

		x1 = r['x1']
		x2 = r['x2']
		y1 = r['y1']
		y2 = r['y2']

		rgba = cmap_boxes(int(r['class']%9))
		rgb = [int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255)]


		sdk.annotations.create(
			project=project_id,
			geometry={
			   "type": "Polygon",
			   "coordinates": [[[x1,y1],[x2,y1], [x2,y2], [x1,y2], [x1,y1]]]
			},
			name=r['class_name'],
			type='image',
			target=r['image_id'],
			stroke=rgb,
			stroke_width=2,
			stroke_opacity=0.8,
			fill=rgb,
			fill_opacity=0.8
			)


if __name__ == "__main__":


	sdk = alteia.SDK(config_path='./config-connections.json')
	project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]
	mission = sdk.missions.search(filter={'project': {'$eq': project.id}})[0]


	WORKING_DIR = Path('./').resolve()
	annotations_dir = WORKING_DIR / 'dataset/exp/'

	export_annotations(project.id, mission.id, 'yolo', annotations_dir)