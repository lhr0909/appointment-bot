FROM python:3.7.9


ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_VERSION=2020.11.15

EXPOSE 5005

RUN  pip install "pipenv==$PIPENV_VERSION"

# Only Copy needed file to docker layer
WORKDIR /opt/rasa-bot
COPY Pipfile /opt/rasa-bot/

# Initialize project
RUN pipenv install --skip-lock

# Add other files to a project
COPY . /opt/rasa-bot/

ENTRYPOINT [ "make" ]
CMD ["server"]
