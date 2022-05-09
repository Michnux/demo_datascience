import cv2
from matplotlib import cm
import matplotlib.pyplot as plt


def draw_boxes(img, boxes, labels, class_names, scores):

	size = img.shape
	print(size)

	for label, [x1, y1, x2, y2], class_name, score in zip(labels, boxes, class_names, scores):

		ycv1 = size[0]-y1
		ycv2 = size[0]-y2
		xcv1 = x1
		xcv2 = x2

		cmap_boxes = cm.get_cmap("Set1") # colour map
		rgba = cmap_boxes(int(label%9))
		bgr = rgba[2]*255, rgba[1]*255, rgba[0]*255

		#box
		line_thickness=5
		tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
		c1, c2 = (int(xcv1), int(ycv1)), (int(xcv2), int(ycv2))
		cv2.rectangle(img, c1, c2, color=bgr, thickness=tl, lineType=cv2.LINE_AA)

		#label on boxes
		txt = class_name # + '  ' + str(round(score,2))
		tf = max(tl - 1, 1)  # font thickness
		t_size = cv2.getTextSize(txt, 0, fontScale=tl / 3, thickness=tf)[0]
		c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
		cv2.rectangle(img, c1, c2, bgr, -1, cv2.LINE_AA)  # filled
		cv2.putText(img, txt, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


	return img



