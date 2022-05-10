import alteia
import json
from pathlib import Path




def export_pdf_report(project_id, mission_id, pdf_report_path):

	#open Alteia sdk
	sdk = alteia.SDK(config_path='./config-connections.json')

	dataset = sdk.datasets.create_file_dataset(name='Annotations_report', project=project_id, mission=mission_id, components=['Annotations_report.pdf'], dataset_format='.pdf')
	sdk.datasets.upload_file(dataset.id, component='Annotations_report.pdf', file_path=pdf_report_path)



if __name__ == "__main__":

	sdk = alteia.SDK(config_path='./config-connections.json')
	project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]

	export_pdf_report('6278e18d1aef750007602a68', '6278e8121aef750007602a6a', './Annotations_report.pdf')
