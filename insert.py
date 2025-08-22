import psycopg2
import csv
import json

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres.",
    "host": "localhost",
    "port": 5432
}

def readjson(rute):

    try:
        with open(rute, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error leyendo JSON: El archivo '{rute}' no existe.")
        exit()
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON desde '{rute}': {e}")
        exit()

def bulk_insert(table_name, data, columns):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Crear un archivo CSV en memoria para `copy_expert`
        with open("temp.csv", "w", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)

        # Leer el archivo CSV y copiarlo a la tabla
        with open("temp.csv", "r") as csv_file:
            copy_query = f"COPY {table_name} ({', '.join(columns)}) FROM STDIN WITH CSV HEADER"
            cursor.copy_expert(copy_query, csv_file)

        conn.commit()
        print("Inserción masiva completada con éxito.")

    except Exception as e:
        print(f"Error durante la inserción masiva: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    table = "currencies"
    json_file = "jsonFiles/new.json"
    columns = ["date", "usd", "eur", "mlc"]

    data = readjson(json_file)

    bulk_insert(table, data, columns)
