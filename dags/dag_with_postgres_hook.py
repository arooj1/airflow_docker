from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
import utils.sql

default_args ={
    "owner":"aaq",
    "retries":0,
    "retry_delays":timedelta(minutes=2)}


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
                                    WHERE emails.received_date::date = CURRENT_DATE::date
                                    LIMIT 2;
                                    
                   """

def my_task():
    hook = PostgresHook(postgres_conn_id="ee_email_conn")
    df = hook.get_pandas_df(sql=ee_emails_query)

    # do what you need with the df....
    print(df.describe())
    

# POSTGRES HOOK WITH CONNECTION
with DAG(
    dag_id= "dag_with_postgres_hook",
    default_args = default_args,
    start_date = datetime(2022,11,30),
    schedule_interval='@daily',    
    tags=["ee_email"]

) as dag:    
    task1 = PythonOperator(
        task_id='postgres_task_using_PostgresHook',
        python_callable=my_task,
    )

task1