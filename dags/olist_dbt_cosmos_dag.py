from airflow import DAG
from airflow.sdk import Asset
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos.constants import LoadMode
from cosmos.profiles import DuckDBUserPasswordProfileMapping
from datetime import datetime, timedelta
import os

# [MODIFICATION] Import du callback WhatsApp
from callbacks import task_failure_whatsapp_alert

# Chemins absolus
DBT_PROJECT_PATH = "/mnt/d/ApacheAirFlowProject/pipeline-projet-olist"
MANIFEST_PATH = "/mnt/d/ApacheAirFlowProject/pipeline-projet-olist/target/manifest.json"
DUCKDB_PATH = "/mnt/d/ApacheAirFlowProject/pipeline-projet-olist/olist.duckdb"
DBT_EXECUTABLE_PATH = "/home/hatem/airflow_venv/bin/dbt"

# Déclaration de l'Asset consommé par ce DAG
olist_raw_asset = Asset("duckdb://raw/olist")

# Configuration du projet dbt
project_config = ProjectConfig(
    dbt_project_path=DBT_PROJECT_PATH,
    manifest_path=MANIFEST_PATH,
)

# Configuration du profil dbt
profile_config = ProfileConfig(
    profile_name="olist_duckdb",
    target_name="dev",
    profile_mapping=DuckDBUserPasswordProfileMapping(
        conn_id="duckdb_default",
        profile_args={
            "path": DUCKDB_PATH,
            "extensions": ["httpfs", "parquet"],
        },
    ),
)

# Configuration de l'exécution
execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)

# Configuration du rendu (lecture du manifeste pour éviter les timeouts)
render_config = RenderConfig(
    load_method=LoadMode.DBT_MANIFEST,
)

default_args = {
    "owner": "hatem",
    "start_date": datetime(2024, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": task_failure_whatsapp_alert,  # [MODIFICATION] Alerte WhatsApp
}

with DAG(
    dag_id="olist_dbt_transform_pipeline",
    default_args=default_args,
    description="Orchestration des transformations dbt (staging -> marts) via Cosmos",
    schedule=[olist_raw_asset],
    catchup=False,
    tags=["olist", "dbt", "cosmos", "duckdb"],
) as dag:

    dbt_transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=render_config,
        operator_args={
            "pool": "duckdb_pool",
        },
    )