import cv2
from matplotlib import cm
import matplotlib.pyplot as plt


classes = ['croquette0', 'croquette1']

def draw_boxes(img, boxes, labels, scores):

	for label, [x1, y1, x2, y2], score in zip(labels, boxes, scores):
		cmap_boxes = cm.get_cmap("Set1") # colour map
		rgba = cmap_boxes(int(label%9))
		bgr = rgba[2]*255, rgba[1]*255, rgba[0]*255
		# cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color=bgr, thickness=1)
		# cv2.putText(frame, classes[int(label)] + '  ' + str(round(score,4)) , (int(x1), int(y1)+8), cv2.FONT_HERSHEY_SIMPLEX, 0.3, bgr, 1)

		#box
		line_thickness=3
		tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
		c1, c2 = (int(x1), int(y1)), (int(x2), int(y2))
		cv2.rectangle(img, c1, c2, color=bgr, thickness=tl, lineType=cv2.LINE_AA)

		#label on boxes
		txt = classes[int(label)] + '  ' + str(round(score,2))
		tf = max(tl - 1, 1)  # font thickness
		t_size = cv2.getTextSize(txt, 0, fontScale=tl / 3, thickness=tf)[0]
		c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
		cv2.rectangle(img, c1, c2, bgr, -1, cv2.LINE_AA)  # filled
		cv2.putText(img, txt, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


	return img



