import sys
import alteia
from pathlib import Path
sys.path.insert(0, './YOLO')
from AlteiaTransactions.ExportAnnotations import export_annotations



if __name__ == "__main__":


	sdk = alteia.SDK(config_path='./config-connections.json')
	project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]
	mission = sdk.missions.search(filter={'project': {'$eq': project.id}})[0]


	WORKING_DIR = Path('./').resolve()
	annotations_dir = WORKING_DIR / 'chess/valid/'

	export_annotations(project.id, '6277e95a1aef750007602a56', 'yolo', annotations_dir)