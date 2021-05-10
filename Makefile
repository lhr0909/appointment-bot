-include .env.local
export

clean:
	rm -rf models/

install:
	pipenv install --skip-lock

server:
	pipenv run rasa run --enable-api $(args)

train:
	pipenv run rasa train $(args)

shell:
	pipenv run rasa shell $(args)

actionserver:
	pipenv run rasa run actions $(args)

test:
	pipenv run python -m actions.calendar
