import os

import pendulum
from airflow.decorators import dag, task


@dag(
    description="Collect running data from strava and store in DuckDB",
    start_date=pendulum.datetime(2024, 9, 8, tz="America/Chicago"),
    schedule="0 */4 * * *",
    catchup=False
)
def running_data_collection():
    @task
    def strava_to_duckdb():
        import os
        import sys
        sys.path.append(os.path.abspath(os.environ["AIRFLOW_HOME"]))

        from include.strava.strava_pipeline import load_strava

        db_file_path = f"{os.getenv('AIRFLOW_HOME')}/data/running.duckdb"
        load_strava(db_file_path)

    strava_to_duckdb()

running_data_collection()
