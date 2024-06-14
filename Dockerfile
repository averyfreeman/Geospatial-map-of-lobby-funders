# prebuilt image at:
# https://hub.docker.com/averyfreeman/wa-lobbbyist-dataset-animations:latest
FROM python:3.12-slim-bookworm

RUN apt update 2>/dev/null | grep packages | cut -d '.' -f 1
RUN apt -y upgrade 2>/dev/null | grep packages | cut -d '.' -f 1
RUN apt install -y ffmpeg 2>/dev/null | grep packages | cut -d '.' -f 1

WORKDIR /app
RUN mkdir /app/recordings

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONWARNINGS="ignore"
ENV PIP_ROOT_USER_ACTION="ignore"

COPY ./bar_chart.py /app/bar_chart.py 
COPY ./geospatial_map.py /app/geospatial_map.py
COPY ./states_no_wa.csv /app/states_no_wa.csv
COPY ./us_states /app/us_states
COPY ./requirements.txt /app/requirements.txt
COPY ./docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh
RUN python -m pip install -r /app/requirements.txt

EXPOSE 8000

ENTRYPOINT /docker-entrypoint.sh