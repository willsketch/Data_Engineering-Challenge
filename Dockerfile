FROM python:3.8.12-slim-buster
COPY career_week_challenge /career_week_challenge
COPY raw_data /raw_data
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD  uvicorn career_week_challenge.api.fast:app --host 0.0.0.0
