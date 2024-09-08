# Airflow on a Raspberry Pi

This is my Airflow deployment intended to run on a Raspberry Pi. This needs to be lightweight due to 
the limited resources available on a Raspberry Pi, so instead of running with Docker, this uses the Airflow 
Python library and the default sqlite database for Airflow.

> The Dockerfile in this repo is used for local development. It emulates the way Airflow is set up on the Raspberry Pi.

## Run Airflow
```bash
airflow webserver -p 8080 & airflow scheduler
```

## Create a user
```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@admin.org
```

## Todo
- [ ] figure out why docker compose didn't work, it said I need to run `airflow db init` even though it was run when building the image. Ended up just running the airflow setup commands myself in the container
