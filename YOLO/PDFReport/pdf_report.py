import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import cv2
from math import floor
from draw_boxes import draw_boxes
import pandas as pd


def pdf_report(df_annotations, images_dir)


	# The PDF document
	pdf = PdfPages('foo.pdf')

	nrows = 3
	ncols = 2

	fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=100, nrows=nrows, ncols=ncols)

	images = os.listdir(images_dir)
	# images = [x for x in images if '.JPG' in x]
	print(images)

	bbox = [150,150, 300, 300]
	color = 'blue'
	boxes = [bbox]
	labels = [1]
	scores = [0.8]

	p = 0

	for k in range(len(images)):

		if floor(k/(nrows*ncols))>p:
			pdf.savefig(fig)
			fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=100, nrows=nrows, ncols=ncols)
			p+=1

		kp = k - p*(nrows*ncols)

		a = floor(kp/ncols)
		b = kp%ncols

		img = cv2.imread(images[k])
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		select = df_annotations[df_annotations['image_name']==images[k]]
		boxes = [[r['x1'], r['y1'], r['x1'], r['y1']] for r in select.iterrows()]
		class_names = select['score'].tolist()
		scores = select['score'].tolist()

		img = draw_boxes(img, boxes, labels, scores)

		ax[a][b].imshow(img)
		ax[a][b].set_title(images[k])

	pdf.savefig(fig)

	pdf.close()


if __name__ == "__main__":

	pdf_report(df_annotations, images_dir)