from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/airflow/dags/app')
from app.file_organizer import organize_postgres_files
from app.file_organizer import organize_csv_files
from app.join_data import merge_orders
from app.file_organizer import rdy_data_to_go

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 3),
    'retries': 5,
    'retry_delay': timedelta(seconds=3)
}

# Define the path to the Meltano project
meltano_project_path = '/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/meltano'
data_base_path = '/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded/raw'

# Initialize the DAG
dag = DAG(
    'meltano_data_pipeline',
    default_args=default_args,
    description='Run Meltano EL jobs with Airflow and organize output',
    schedule_interval=None,  # Run manually or set a cron schedule
)

# Task to extract and load data from PostgreSQL to CSV
extract_load_postgres = BashOperator(
    task_id='extract_load_postgres',
    bash_command=f'cd {meltano_project_path} && meltano el tap-postgres target-csv',
    dag=dag,
)

# Task to move PostgreSQL CSV files to the structured folder
organize_postgres_files_task = PythonOperator(
    task_id='organize_postgres_files',
    python_callable = organize_postgres_files,
    op_args=['/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded'],
    dag=dag,
    )

# Task to extract and load data from CSV to CSV
extract_load_csv = BashOperator(
    task_id='extract_load_csv',
    bash_command=f'cd {meltano_project_path} && meltano el tap-csv target-csv',
    dag=dag,
)


# Task to move CSV files to the structured folder
organize_csv_files_task = PythonOperator(
    task_id='organize_csv_files',
    python_callable = organize_csv_files,
    op_args=['/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded'],
    dag=dag,
    )

# Task to merge the data from orders and order_detail 
merge_orders_task = PythonOperator(
    task_id='merge_orders_task',
    python_callable=merge_orders,
    dag=dag
)

# Task to merge the data from orders and order_detail 
rdy_data_task = PythonOperator(
    task_id='rdy_data_to_postgres',
    python_callable=rdy_data_to_go,
    dag=dag
)

# Task to extract and load data from CSV to CSV
upload_golden_db = BashOperator(
    task_id='upload_golden_to_postgres',
    bash_command=f'cd {meltano_project_path} && meltano el tap-csv--golden target-postgres',
    dag=dag,
)

# Define task dependencies
extract_load_postgres >> organize_postgres_files_task
extract_load_csv >> organize_csv_files_task

merge_orders_task.set_upstream([extract_load_postgres, organize_postgres_files_task, extract_load_csv, organize_csv_files_task])

merge_orders_task >> rdy_data_task >> upload_golden_db 