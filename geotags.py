import exif
from exif import Image
import os
from pathlib import Path




def read_exif(pict_name):
	with open(pict_name, 'rb') as image_file:
		my_exif = exif.Image(image_file)

	print(my_exif.list_all())

	for k in my_exif.list_all():
		if k!='components_configuration' and k!='maker_note' and k!='flashpix_version' and k!='scene_type':
			print(k, my_exif[k])

	return my_exif




def add_fake_geotag(pict_path, pict_name, out_path):


	with open(pict_path/pict_name, 'rb') as image_file:
		my_image = exif.Image(image_file)

	# print(my_image.has_exif)
	# print(my_image.list_all())


	my_image.make='Apple'
	my_image.model='iPhone 12 Pro'
	my_image.orientation=1#Orientation.TOP_LEFT
	my_image.datetime = '2022:04:05 11:51:59'
	my_image.gps_latitude_ref='N'
	my_image.gps_latitude=(43.0, 33.0, 14.02)
	my_image.gps_longitude_ref='E'
	my_image.gps_longitude=(1.0, 30.0, 34.18)
	my_image.gps_altitude_ref=5#'GpsAltitudeRef.ABOVE_SEA_LEVEL'
	my_image.gps_altitude=149.244

	# print(my_image.has_exif)
	# print(my_image.list_all())


	with open(out_path / pict_name, 'wb') as new_image_file:
		new_image_file.write(my_image.get_file())



if __name__ == "__main__":

	# my_exif = read_exif('IMG_9559.JPG')

	dir_path = Path('./chess/train/images/')
	out_path = Path('./chess_geo/train/')
	files = os.listdir(dir_path)
	print(files)
	if not os.path.exists(out_path):
		os.mkdir(out_path)

	for f in files:
		add_fake_geotag(dir_path, f, out_path)
