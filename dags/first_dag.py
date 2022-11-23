# instantiate the class DAG 
from airflow import DAG # import
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
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
# create instance
with DAG(
    dag_id= "our_first_dag_v3",
    default_args = default_args,
    description= "first sample dag instance for testing purposes",
    start_date = datetime(2022,11,20,23),
    schedule_interval='@daily'


) as dag: 
    task1 = BashOperator(
        task_id='first_task',
        bash_command = "echo hello world, this is the first task!"
    )
    task2 = BashOperator(
        task_id='second_task',
        bash_command = "echo hey I am the 2nd task and will run after task-1"
    )
    task1 >> task2

'''
Once DAG is instantiated with some inital information/ variables. Let's create our first task. 
- First tasks is a simple bash command using bash operator. 
a hello message on the terminal 
'''    
