import os
import subprocess
import sys
from pathlib import Path
import alteia

from AlteiaTransactions.ImportDataset import import_dataset
from AlteiaTransactions.ImportWeights import import_weights
from AlteiaTransactions.ExportPDFReport import export_pdf_report
from AlteiaTransactions.ExportAnnotations import export_annotations, convert_annotations
from PDFReport.pdf_report import pdf_report


# sys.path.insert(1, './yolov5')







def run(project_id, mission_id, WORKING_DIR):

	dataset_path = WORKING_DIR / 'dataset'
	project_path = WORKING_DIR / 'project'
	weights_path = WORKING_DIR / 'input_yv5.pt'

	import_dataset(project_id, mission_id, 'yolo_inference', dataset_path)
	# import_weights(mission_id, mission_id, weights_dir)

	cmd = "python3 yolov5/detect.py --weights "+str(weights_path)+ \
									" --source "+str(dataset_path)+"/images"+\
									" --save-txt --save-conf"+\
									" --project "+str(project_path) # --nosave True"
	subprocess.run(cmd, shell=True)

	df_annotations = convert_annotations(project_id, mission_id, annotations_format='yolo', annotations_dir=project_path / 'exp')
	export_annotations(project_id, mission_id, df_annotations)
	pdf_report(df_annotations, images_dir=dataset_path / 'images', WORKING_DIR=WORKING_DIR)
	export_pdf_report(project_id, mission_id, WORKING_DIR / 'Annotations_report.pdf')


if __name__ == "__main__":


	sdk = alteia.SDK(config_path='./config-connections.json')
	project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]
	mission = sdk.missions.search(filter={'project': {'$eq': project.id}})[0]

	WORKING_DIR = Path('./').resolve()
	run(project.id, mission.id, WORKING_DIR)
