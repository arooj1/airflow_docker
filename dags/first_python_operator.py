# instantiate the class DAG 
from airflow import DAG # import
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
'''
Imagine if we want to 
    - start our dag from November 21, 2022 at 2pm and
    - it should run @daily

'''
default_args = {
    'owner':'aaq',
    'retries': 5,
    'retry_delay': timedelta(minutes=2) # wait time is set to 2 minutes

}
# Python functions for the python operator
def greet(age, ti):
    name = ti.xcom_pull(task_ids='get_name')
    
    print("First pythonOperator based task in the airflow")
    print(f'Welcome {name}. With your {age}, you have qualified for the gift ')

def get_name():
    return 'Awa'


# create instance
with DAG(
    dag_id= "our_first_python_operator__dag_v4",
    default_args = default_args,
    description= "first sample dag instance for testing purposes",
    start_date = datetime(2022,11,20,23),
    schedule_interval='@daily'


) as dag: 
    task1 = PythonOperator(
         task_id='first_python_operator_task',
         python_callable=greet,
         op_kwargs={'age':20}
    )
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name,
        
    )
    task2 >> task1

'''
Once DAG is instantiated with some inital information/ variables. Let's create our first task. 
- First tasks is a simple bash command using bash operator. 
a hello message on the terminal 
'''    
