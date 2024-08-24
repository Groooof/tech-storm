FROM python:3.11-slim-bullseye as build-stage-base
WORKDIR /opt/techstorm/backend
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

FROM build-stage-base as tests-run
COPY test-requirements.txt test-requirements.txt
RUN pip install -r test-requirements.txt

FROM build-stage-base as local-run
CMD ["uvicorn", "app:get_app", "--reload", "--host", "0.0.0.0", "--port", "8008"]

FROM build-stage-base as server-run
CMD ["uvicorn", "app:get_app", "--host", "0.0.0.0", "--port", "8008"]
