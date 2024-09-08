from airflow.decorators import dag, task
import pendulum

@dag(
    start_date=pendulum.datetime(2024, 9, 8, tz="America/Chicago"),
    schedule="@daily",
    catchup=False
)
def test():
    @task
    def say_hello():
        print("hello")

    say_hello()

test()
