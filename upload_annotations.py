import sys
import alteia
from pathlib import Path
sys.path.insert(0, './YOLO')
from AlteiaTransactions.ExportAnnotations import export_annotations, convert_annotations



if __name__ == "__main__":


	sdk = alteia.SDK(config_path='./config-connections.json')
	project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]
	mission = sdk.missions.search(filter={'project': {'$eq': project.id}})[0]


	WORKING_DIR = Path('./').resolve()
	annotations_dir = WORKING_DIR / 'chess_geo/train/'


	df_annotations = convert_annotations('6278e18d1aef750007602a68', '6278e1c444872f0008e07a43', 'yolo', annotations_dir)
	export_annotations('6278e18d1aef750007602a68', '6278e1c444872f0008e07a43', df_annotations)