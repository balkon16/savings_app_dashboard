from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.dummy import DummyOperator

dag = DAG(
    dag_id="savings_app_dag",
    description="Import spreadsheet based data into a database.",
    schedule_interval="5 4 * * *",  # TODO: TBD
    start_date=days_ago(1)
)

start = DummyOperator(task_id="START", dag=dag)
end = DummyOperator(task_id="END", dag=dag)

start >> end


