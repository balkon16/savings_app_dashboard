from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.dummy import DummyOperator

# TODO: Na podstawie kolumn oznaczonych jako `first_insert` tworzę/uaktualniam słowniki, np. ticker->pełna nazwa

dag = DAG(
    dag_id="savings_app_dag",
    description="Import spreadsheet based data into a database.",
    schedule_interval="5 4 * * *",  # TODO: TBD
    start_date=days_ago(1)
)

def _read_exchange_rate_sheet():
    pass

start = DummyOperator(
    task_id="START",
    dag=dag)


end = DummyOperator(
    task_id="END",
    dag=dag)

start >> end
