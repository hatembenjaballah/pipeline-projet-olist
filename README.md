# 🛒 Pipeline de données E-commerce Olist (ELT)

Ce projet est un pipeline de données complet (ELT) construit localement, simulant une architecture moderne de type Modern Data Stack.

## 🏗️ Architecture

1. **Ingestion** : Un DAG Airflow charge 9 fichiers CSV bruts dans un schéma `raw` (DuckDB).
2. **Transformation** : `dbt` transforme les données en modèles analytiques (staging → intermediate → marts).
3. **Orchestration** : Astronomer Cosmos orchestre dbt dans Airflow (1 tâche Airflow = 1 modèle dbt).
4. **Alerting** : Un email est envoyé automatiquement en cas d'échec d'une tâche.

### 📊 Schéma de l'architecture

```mermaid
graph TD
    %% Définition des sources
    subgraph Sources["📁 Sources de données"]
        CSV["9 Fichiers CSV Olist"]
    end

    %% Définition de l'orchestrateur Airflow
    subgraph Airflow["🚀 Apache Airflow (Orchestration)"]
        DAG_Ingest["DAG: olist_ingestion_pipeline<br/>(PythonOperator)"]
        DAG_Transform["DAG: olist_dbt_transform_pipeline<br/>(Astronomer Cosmos)"]
        AlertCallback["🚨 Callback: task_failure_whatsapp_alert"]
    end

    %% Définition de l'entrepôt de données
    subgraph DuckDB["🦆 Base de données DuckDB"]
        Raw[("Schéma: raw<br/>(Tables brutes)")]
        Staging[("Schéma: staging<br/>(Vues de nettoyage)")]
        Intermediate[("Schéma: intermediate<br/>(Vues de jointures)")]
        Marts[("Schéma: marts<br/>(Tables analytiques)")]
    end

    %% Définition des alertes
    subgraph Alerts["📱 Alerting"]
        WhatsApp["Message WhatsApp<br/>(via TextMeBot)"]
    end

    %% Flux d'ingestion
    CSV -->|Extract & Load| DAG_Ingest
    DAG_Ingest -->|Ingestion SQL| Raw

    %% Déclenchement automatique (Data-Aware)
    Raw -.->|Déclenchement via Asset| DAG_Transform

    %% Flux de transformation dbt (CORRECTION ICI : ajout des guillemets)
    DAG_Transform -->|1 Tâche = 1 Modèle| Staging
    Staging -->|"dbt ref()"| Intermediate
    Intermediate -->|"dbt ref()"| Marts

    %% Flux d'alerting
    DAG_Ingest -.->|En cas d'échec| AlertCallback
    DAG_Transform -.->|En cas d'échec| AlertCallback
    AlertCallback -->|Requête HTTP| WhatsApp

    %% Style des blocs
    classDef source fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef airflow fill:#e3f2fd,stroke:#1976d2,stroke-width:2px;
    classDef db fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef alert fill:#ffebee,stroke:#d32f2f,stroke-width:2px;

    class CSV source;
    class DAG_Ingest,DAG_Transform,AlertCallback airflow;
    class Raw,Staging,Intermediate,Marts db;
    class WhatsApp alert;
```
## 🛠️ Stack Technique
- **Orchestration** : Apache Airflow 3.x
- **Transformation** : dbt Core & dbt-duckdb
- **Intégration dbt** : Astronomer Cosmos
- **Base de données** : DuckDB (fichier local)

## 🚀 Comment exécuter le projet
1. Activer l'environnement virtuel : `source airflow_venv/bin/activate`
2. Démarrer Airflow : `airflow standalone`
3. Lancer l'ingestion : Déclencher le DAG `olist_ingestion_pipeline`
4. Le DAG `olist_dbt_transform_pipeline` se déclenchera automatiquement à la fin de l'ingestion.
