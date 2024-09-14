FROM python:3.11.9-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AIRFLOW_HOME='/airflow'

WORKDIR /airflow
COPY airflow-requirements.txt /airflow/
COPY . /airflow/

RUN ./install.sh
RUN airflow db init
RUN airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@admin.org

RUN pip install -r requirements.txt


CMD ["tail", "-f","/dev/null"]
