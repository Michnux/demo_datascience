import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import cv2
from math import floor
import sys
sys.path.insert(0, '..')
from PDFReport.draw_boxes import draw_boxes
from AlteiaTransactions.ExportAnnotations import convert_annotations
import pandas as pd
import alteia
from pathlib import Path




def pdf_report(df_annotations, images_dir, WORKING_DIR):


	# The PDF document
	pdf = PdfPages(WORKING_DIR / 'Annotations_report.pdf')

	nrows = 3
	ncols = 2

	fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=100, nrows=nrows, ncols=ncols)

	images = os.listdir(images_dir)


	p = 0 #current page of the pdf file

	for k in range(len(images)):

		if floor(k/(nrows*ncols))>p:
			pdf.savefig(fig)
			plt.close('all')
			fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=100, nrows=nrows, ncols=ncols)
			p+=1

		kp = k - p*(nrows*ncols)

		a = floor(kp/ncols)
		b = kp%ncols

		img = cv2.imread(str(images_dir / images[k]))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		select = df_annotations[df_annotations['image_name']==images[k][:-4]]
		boxes = [[r['x1'], r['y1'], r['x2'], r['y2']] for _,r in select.iterrows()]
		labels = select['class'].tolist()
		class_names = select['class_name'].tolist()
		scores = select['score'].tolist()

		img = draw_boxes(img, boxes, labels, class_names, scores)

		# plt.imshow(img)
		# plt.show()

		ax[a][b].imshow(img)
		ax[a][b].set_title(images[k], fontdict={'fontsize': 7})

	pdf.savefig(fig)

	#make a histogram of total number of each annotation
	fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=100, nrows=2, ncols=1)


	# pivot = df_annotations.pivot(index='class_names', values='class_names', aggfunc='count')
	class_names = df_annotations['class_name'].drop_duplicates().tolist()
	counts = [df_annotations[df_annotations['class_name']==c].shape[0] for c in class_names]

	ax[0].bar(range(len(counts)), counts, tick_label=class_names)
	ax[0].set_xticklabels(class_names, rotation=45, ha='right', fontdict={'fontsize': 7})
	pdf.savefig(fig)

	pdf.close()




if __name__ == "__main__":

	sdk = alteia.SDK(config_path='./config-connections.json')
	# project = sdk.projects.search(filter={'name': {'$eq': 'Demo_datascience'}})[0]
	# mission = sdk.missions.search(filter={'project': {'$eq': project.id}})[0]

	WORKING_DIR = Path('./').resolve()
	annotations_dir = Path('C:\\Users\\michael.delagarde\\Documents\\DEV\\DemoDataScience\\chess\\valid')

	df_annotations = convert_annotations('6242fedbc55a3c0007254175', '6277e95a1aef750007602a56', annotations_format='yolo', annotations_dir=annotations_dir)
	# export_annotations(df_annotations)
	print(df_annotations.columns)
	pdf_report(df_annotations, images_dir=annotations_dir/'images', WORKING_DIR=Path('./'))
