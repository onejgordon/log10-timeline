# Log Timeline

Python script to generate log-scale PDF timelines from arbitrary event data

![log timeline screenshot](https://github.com/onejgordon/log-timeline/blob/master/static/screenshot.png)

## Usage

* Create a JSON data file with events (see data/human_evolution.json as an example)
* Install requirements - `pip install -r requirements.txt`
* `python logtimeline.py` generates a PDF in the output directory

## TODO

* Web-app via Google cloud functions
* Doc site

## Misc

### Deploying to AWS Lambda

* Zip contents of root directory & upload to lambda (https://console.aws.amazon.com/lambda/home)
* Run test function