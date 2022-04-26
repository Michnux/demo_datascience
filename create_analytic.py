import alteia



sdk = alteia.SDK(config_path='./config-connections.json')



analytic = sdk.analytics.search(name="alteiademo/run_yolov5")
if len(analytic)>0:
	analytic=analytic[0]
	sdk.analytics.delete(analytic=analytic.id)

analytic = sdk.analytics.search(name="alteiademo/train_yolov5")
if len(analytic)>0:
	analytic=analytic[0]
	sdk.analytics.delete(analytic=analytic.id)


sdk.analytics.create(name="alteiademo/run_yolov5",
	version="1.0.0",
	display_name="run_yolov5",
	description="Runs yolov5 (object detection) on a survey",
	docker_image="registry-1.docker.io/michaeldelagarde/yv5:latest",
	company="5c1a2567b3c575583e8a650d",
	instance_type='small',
	volume_size=20,
	inputs=[{
			"name": "weights",
			"display_name": "weights",
			"description": ".pt weights file",
			"scheme": {
				"type": "string", "pattern": "^[0-9a-f]{24}$"
			},
			"source": {
				"service": "data-manager",
				"resource": "dataset",
				"scheme": {
					"type": "object",
					"category": "object detection",
					"properties": {"type": {"const": "file"}}, ####
					"required": ["type"]
				},
			},
			"required": True
		},
	],
	parameters=[
	],
	deliverables=[
	],
	# tags=["croquette"],
	groups=["DATA SCIENCE"])


sdk.analytics.create(name="alteiademo/train_yolov5",
	version="1.0.0",
	display_name="train_yolov5",
	description="Runs yolov5 (object detection) on a survey",
	docker_image="registry-1.docker.io/michaeldelagarde/yv5:latest",
	company="5c1a2567b3c575583e8a650d",
	instance_type='small',
	volume_size=20,
	inputs=[{
			"name": "weights",
			"display_name": "weights",
			"description": ".pt weights file to be used as initial model for training (Default: yolov5s.pt)",
			"scheme": {
				"type": "string", "pattern": "^[0-9a-f]{24}$"
			},
			"source": {
				"service": "data-manager",
				"resource": "dataset",
				"scheme": {
					"type": "object",
					"category": "object detection",
					"properties": {"type": {"const": "file"}}, ####
					"required": ["type"]
				},
			},
			"required": True
		},
	],
	parameters=[
	{
		"name": "epochs",
		"display_name": "Number of epochs",
		"description": "Start with 300 epochs. If this overfits early then you can reduce epochs. If overfitting does not occur after 300 epochs, train longer, i.e. 600, 1200 etc epochs.",
		"required": True,
		"scheme": {
			"type": "string",
			"pattern": "^[0-9]{24}$"
		}
	 },
	{
		"name": "image_size",
		"display_name": "Number of epochs",
		"description": " COCO trains at native resolution of --img 640, though due to the high amount of small objects in the dataset it can benefit from training at higher resolutions such as --img 1280. If there are many small objects then custom datasets will benefit from training at native or higher resolution. Best inference results are obtained at the same --img as the training was run at, i.e. if you train at --img 1280 you should also test and detect at --img 1280",
		"required": False,
		"scheme": {
			"type": "string",
			"pattern": "^[0-9]{24}$"
		}
	 },
	],
	deliverables=[
	],
	# tags=["croquette"],
	groups=["DATA SCIENCE"])