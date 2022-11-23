## AIRFLOW DOCKER
### Documentation
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html 

### Video Tutorial
https://www.youtube.com/watch?v=K9AnJ9_ZAXE&t=471s 

## STEPS TO FOLLOW
- install docker and make sure it is running on you machine
- then create a folder and copy `docker-compose.yml` file from the airflow-docker official website
-  Make changes in the docker file if required.
- check if the docker is running by typing following in the terminal
`docker --version`
`docker-compose --version`

- initialize docker base database (which is by defualt is sqlite)
`docker-compose -u airflow-init`
The output of this file should be `exited with code 0` which means database is initialised. 
- run airflow in docker 
`docker-compose up -d` 
- check what is running inside the docker
`docker ps`

- open web browser and check if the airflow is running: `localhost:8080`. 

- You will notice in the browser that a lot of sample DAGs are running. If you want to remove all sample DAGS and create your own then type this in the terminal
`docker-compose down -v` 
and then change this from `true` to `false` in docker-compose.yml file
`AIRFLOW__CORE__LOAD_EXAMPLES: 'false'`

- re initiate docker db:
    - `docker-compose -u airflow-init`
    - `docker-compose up -d`  
