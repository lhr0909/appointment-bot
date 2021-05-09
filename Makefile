.EXPORT_ALL_VARIABLES:

RASA_DUCKLING_HTTP_URL = http://localhost:8000
RASA_X_PASSWORD = Qwe123123
ACTION_ENDPOINT = http://localhost:5055/webhook
RECOGNIZERS_SERVICE_URL = http://localhost:7000/recognize/number

install:
	pipenv install --skip-lock

clean:
	rm -rf models/

server:
	poetry run rasa run --enable-api $(args)

train:
	pipenv run rasa train $(args)

shell:
	pipenv run rasa shell $(args)

actionserver:
	pipenv run rasa run actions $(args)
