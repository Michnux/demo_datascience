import alteia
import os
import string
import pandas as pd




ds_formats = ['SuperAnnotate', 'yolo_inference', 'yolo_training']


def import_dataset(project_id, mission_id, ds_format, destination_folder):

	#create destination dir if doesn't exist
	if not os.path.isdir(destination_folder):
		os.mkdir(destination_folder)

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

	df_images=df_images.drop_duplicates()

	if ds_format=='SuperAnnotate': #generate .sa file in image forlder
		images_sa = []

	#create dir: dataset/images
	if not os.path.isdir(destination_folder+'images/'):
		os.mkdir(destination_folder+'images/')

	for d in images_datasets:
		try:
			path = sdk.datasets.download_image_as_jpeg(d.id, target_path=destination_folder+'images/')
		except FileExistsError as e:
			path = e.args[0][16:]
		

		if ds_format=='SuperAnnotate': #generate thumbnail in images folder
			try:
				thumb_name = "thmb_"+path.split('/')[-1]
				thumb_path = sdk.datasets.download_preview(d.id, target_path=destination_folder+'images/thumb/', target_name=thumb_name)
			except FileExistsError as e:
				thumb_path = e.args[0][16:]

		if ds_format=='SuperAnnotate': #generate .sa file in images forlder
			images_sa.append({"srcPath":pwd+path,
							"name":path.split('/')[-1],
							"imagePath":pwd+path,
							"thumbPath":pwd+thumb_path,
							"valid":True})

	if ds_format=='SuperAnnotate': #generate .sa file in image forlder
		import json
		json_string = json.dumps(images_sa)
		json_string = json_string.replace('/', '\\\\')
		json_string = json_string.replace('\'True\'', 'true')

		text_file = open(destination_folder+'images/images.sa', "w")
		text_file.write(json_string)
		text_file.close()



	if ds_format=='yolo_training': #get annotations associated with dataset images

		# annotations = sdk.annotations.search(filter={'project': {'$eq': project_id}, 'mission': {'$eq': mission_id}}) #doesn't work
		annotations = sdk.annotations.search(filter={'project': {'$eq': project_id}}) #could be filtered by flight?
		annotations = [a for a in annotations if a.type=='image']

		#yolo format
		#class x_center y_center width height #[0,1]

		df_annotations = pd.DataFrame()

		for an in annotations:

			df_annotations = pd.concat([df_annotations, pd.DataFrame({
										'class_name':[an.name],
										'x1':[min(an.geometry['coordinates'][0][0][0],an.geometry['coordinates'][0][1][0],an.geometry['coordinates'][0][2][0],an.geometry['coordinates'][0][3][0])],
										'y1':[min(an.geometry['coordinates'][0][0][1],an.geometry['coordinates'][0][1][1],an.geometry['coordinates'][0][2][1],an.geometry['coordinates'][0][3][1])],
										'x2':[max(an.geometry['coordinates'][0][0][0],an.geometry['coordinates'][0][1][0],an.geometry['coordinates'][0][2][0],an.geometry['coordinates'][0][3][0])],
										'y2':[max(an.geometry['coordinates'][0][0][1],an.geometry['coordinates'][0][1][1],an.geometry['coordinates'][0][2][1],an.geometry['coordinates'][0][3][1])],
										'image_id':an.target['id']
									})])

		df_classes = pd.DataFrame()
		df_classes['class_name'] = df_annotations['class_name'].drop_duplicates()
		df_classes['class']=range(df_classes.shape[0])

		#df_annotations < - - df_images
		df_annotations = df_annotations.join(df_images.set_index('image_id')[['image_name', 'size_x', 'size_y']], on='image_id')

		#df_annotations < - - classes
		df_annotations = df_annotations.join(df_classes.set_index('class_name')[['class']], on='class_name')

		df_annotations['x_center']= (df_annotations['x1']+df_annotations['x2'])/2/df_annotations['size_x']
		df_annotations['y_center']= (df_annotations['y1']+df_annotations['y2'])/2/df_annotations['size_y']
		df_annotations['width']= (-df_annotations['x1']+df_annotations['x2'])/df_annotations['size_x']
		df_annotations['height']= (-df_annotations['y1']+df_annotations['y2'])/df_annotations['size_y']


		print(destination_folder+'annotations/')
		#create yolo annotations foleder and files
		if not os.path.isdir(destination_folder+'annotations/'):
			print('creating folder')
			os.mkdir(destination_folder+'annotations/')

		for im in df_images['image_name'].tolist():
			dfo = df_annotations[df_annotations['image_name']==im]
			dfo[['class', 'x_center', 'y_center', 'width', 'height']].to_csv(destination_folder+'annotations/'+im+'.txt', sep=' ', index=False, header=False)#remove header & index



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

	import_dataset(project.id, mission.id, 'yolo_training', destination_folder)