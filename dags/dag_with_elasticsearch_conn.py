"""
Example Airflow DAG for Elasticsearch Query.
"""
from __future__ import annotations
from utils.elastic_search_utils import EsManagement
import os
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


from datetime import datetime, timedelta

#ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "elasticsearch_dag"
CONN_ID = "local_elastic_conn"

default_args ={
    "owner":"aaq",
    "retries":0,
    "retry_delays":timedelta(minutes=2)}

def access_elastic_conn():
    es_connection = EsManagement()
    print("========= Connection Established ========")
    document_indices = es_connection.es_client.indices.get_mapping(index="bbm_aiml_ee_email")
    return document_indices
	


with DAG(
    dag_id= "dag_with_elastic_hook_PythonOperator",
    default_args = default_args,
    start_date = datetime(2022,11,30),
    schedule_interval='@daily',    
    tags=["ee_email"]

) as dag:
    task1 = PythonOperator(
            task_id='reading_data_from_elastic',
            python_callable=access_elastic_conn           
           

    )

task1

