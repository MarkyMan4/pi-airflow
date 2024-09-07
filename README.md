# Airflow on a Raspberry Pi

Database, logs, and `airflow.cfg` are located here:
`~/airflow/`

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
