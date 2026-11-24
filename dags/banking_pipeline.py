
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="ksa_banking_data_pipeline",
    default_args=default_args,
    description="KSA retail banking end-to-end data pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["banking", "data-engineering"],
) as dag:

    run_banking_pipeline = BashOperator(
        task_id="run_banking_pipeline",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m scripts.pipeline"
        ),
    )