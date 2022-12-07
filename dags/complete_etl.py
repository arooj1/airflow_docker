'''
COMPLETE EXTRACTION-TRANSFORMATIO-LOAD PROCESS 
1- Data extracted from Postgres
2- Data transformation in pandas
3- Data loading in ElasticSearch 

'''

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
import utils.sql
from utils.data_transformation_utils import PandasUtils
from utils.elastic_search_utils import EsManagement
import json

default_args ={
    "owner":"aaq",
    "retries":0,
    "retry_delays":timedelta(minutes=2)}


# =========================   BASIC INFORMATION ======================================
'''
ElasticSearch index will be different for each project. Therefore, enter the name of the index relevant to the project. 
SQL_Query (ee_emails_query) data query to extract from PostgreSQL 
'''
# ElasticSearch Index
index_name = "bbm_aiml_ee_email"
# QUERY
ee_emails_query = """SELECT 
                            emails.id AS ID,
                            emails.received_date,
                            emails.order_id,
                            emails.priority,
                            static_topic.name AS topic_name,
                            emails.upload_date,
                            emails.actioned_by_id,
                            emails.assigned_date, 
                            emails.actioned_date, 
                            emails.prediction, 
                            emails.triaged_date,
                            emails.uploaded_to_pathway, 
                            emails.task_id,
                            emails.triaged_by_id,
                            emails.action_type,
                            response.sent_dt,
                            response.template_type 
                        FROM project_email AS emails
                        LEFT JOIN
                            project_email AS response 
                        ON 
                            emails.id = response.response_id 
                            INNER JOIN 
                                project_topic AS topics
                            ON 
                                emails.selected_topic_id = topics.id 
                                INNER JOIN 
                                    project_statictopic AS static_topic 
                                ON 
                                    topics.static_topic_id = static_topic.id AND emails.received_date is not Null AND emails.selected_topic_id is not Null
                                    WHERE emails.received_date::date = CURRENT_DATE::date;
                                    
                   """



# ================= PROCESS DEFINED IN THIS TASK (Extraction-Transformation-Load) =======================
def my_task():

    # STEP 1: Data Extraction from PostgreSQL
    hook = PostgresHook(postgres_conn_id="ee_email_conn")
    dataframe = hook.get_pandas_df(sql=ee_emails_query)

    # STEP 2: Data Transformation in Pandas
    print(dataframe.describe())
    pandas_util = PandasUtils(dataframe)
    transformed_dataframe = pandas_util()
    print("DATA TRANSFORMATION ========= DONE ")
    print(transformed_dataframe.info())


    # STEP 3: Data Load in ElasticSearch
    es_connection = EsManagement()
    print("CONNECTION ESTABLISHED ======= DONE")
    document_indices = es_connection.es_client.indices.get_mapping(index=index_name)
    print(f"Writing {len(transformed_dataframe.index)} documents to ES index {index_name}")

    for doc in transformed_dataframe.apply(lambda x: x.to_dict(), axis=1):
        es_connection.es_client.index(index=index_name, body=json.dumps(doc, default=str))
   
    print(f'DOCUMENTS LOADED TO THE ELASTICSEARCH indices')
    

with DAG(
    dag_id= "etl_complete_dag",
    default_args = default_args,
    start_date = datetime(2022,12,6),
    schedule_interval='@daily',    
    tags=["ee_email"]

) as dag:    
    task = PythonOperator(
        task_id='complete_etl_process_task',
        python_callable=my_task,
    )

task