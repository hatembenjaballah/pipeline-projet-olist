from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sdk import Asset  # Utilisation de Asset pour Airflow 3
from datetime import datetime, timedelta
import sys
import os

# Ajout du dossier scripts au path Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from ingest_olist import ingest_csv_to_duckdb

# [MODIFICATION] Import du callback WhatsApp
from callbacks import task_failure_whatsapp_alert

# Chemins absolus
DUCKDB_PATH = "/mnt/d/ApacheAirFlowProject/pipeline-projet-olist/olist.duckdb"
DATASET_DIR = "/mnt/d/ApacheAirFlowProject/pipeline-projet-olist/dataset"

# Déclaration de l'Asset produit par ce DAG
olist_raw_asset = Asset("duckdb://raw/olist")

default_args = {
    'owner': 'hatem',
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': task_failure_whatsapp_alert,  # [MODIFICATION] Alerte WhatsApp
}

with DAG(
    dag_id='olist_ingestion_pipeline',
    default_args=default_args,
    description='Ingestion des CSV Olist dans DuckDB (Schema raw)',
    schedule='@daily',
    catchup=False,
    tags=['olist', 'ingestion', 'duckdb'],
) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_csv_to_duckdb',
        #python_callable=ingest_csv_to_duckdb,
        python_callable=lambda **kwargs: (_ for _ in ()).throw(Exception("Test d'alerte WhatsApp")), #test Alert WhatsApp
        op_kwargs={
            'duckdb_path': DUCKDB_PATH,
            'dataset_dir': DATASET_DIR
        },
        outlets=[olist_raw_asset],
    )