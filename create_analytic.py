import alteia



sdk = alteia.SDK(config_path='./config-connections.json')


analytic = sdk.analytics.search(name="alteiademo/inference_yv5")
if len(analytic)>0:
	analytic=analytic[0]
	sdk.analytics.delete(analytic=analytic.id)

sdk.analytics.create(name="alteiademo/inference_yv5",
	version="1.0.0",
	display_name="inference_yv5",
	description="Runs yolov5 (object detection) on a survey",
	docker_image="registry-1.docker.io/michaeldelagarde/inference_yv5:latest",
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