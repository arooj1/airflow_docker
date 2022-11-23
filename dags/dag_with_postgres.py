from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner':'aaq',
    'retries': 5,
    'retry_delay': timedelta(minutes=2) # wait time is set to 2 minutes

}

with DAG(
    dag_id= "dag_with_postgres_operator",
    default_args = default_args,
    start_date = datetime(2022,11,22),
    schedule_interval='@daily'

) as dag:
    task1 = PostgresOperator(
            task_id='create_postgres_table',
            postgres_conn_id='postgrs_local',
            sql = """
                create table if not exists dag_runs (
                    dt date,
                    dag_id character varying,
                    primary key(dt, dag_id))
            
            """

    )

    task1