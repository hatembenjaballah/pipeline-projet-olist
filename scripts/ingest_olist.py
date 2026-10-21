import duckdb
import os

def ingest_csv_to_duckdb(duckdb_path: str, dataset_dir: str):
    """
    Lit les fichiers CSV Olist et les charge dans le schéma 'raw' de DuckDB.
    """
    # Connexion à la base DuckDB
    con = duckdb.connect(duckdb_path)
    
    # Création du schéma 'raw' s'il n'existe pas
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    
    # Liste des fichiers CSV et de leurs tables cibles
    csv_files = {
        "olist_customers_dataset.csv": "customers",
        "olist_geolocation_dataset.csv": "geolocation",
        "olist_order_items_dataset.csv": "order_items",
        "olist_order_payments_dataset.csv": "order_payments",
        "olist_order_reviews_dataset.csv": "order_reviews",
        "olist_orders_dataset.csv": "orders",
        "olist_products_dataset.csv": "products",
        "olist_sellers_dataset.csv": "sellers",
        "product_category_name_translation.csv": "product_category_name_translation"
    }
    
    for csv_file, table_name in csv_files.items():
        file_path = os.path.join(dataset_dir, csv_file)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Fichier introuvable : {file_path}")
            
        print(f"Ingestion de {csv_file} dans raw.{table_name}...")
        
        # Utilisation de read_csv_auto pour lire et créer la table directement
        # On écrase la table si elle existe déjà pour rendre le job idempotent
        con.execute(f"""
            CREATE OR REPLACE TABLE raw.{table_name} AS 
            SELECT * FROM read_csv_auto('{file_path}', HEADER=TRUE);
        """)
        
    con.close()
    print("Ingestion terminée avec succès.")