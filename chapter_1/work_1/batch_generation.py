import random # crea valores aleatorios
import csv # para leer archivos .cssv
import logging # para tener log y poder monitorear
import uuid # crea identtificadores únicos
import polars as pl # librería de DataFrames

from faker import Faker # Para crear datos
from datetime import date, datetime, timedelta

# Configuración de logs. 
# Cómo se van a mostrar los logs
logging.basicConfig(
    level=logging.INFO, # Se van a ver los logs de tipo info o los más importantes
    format= '%(asctime)s - %(levelname)s - %(messege)s', # Cómo se va a guardar el mensaje y se van a mostrar
    datefmt='%Y-%m-%d %H:%M:%S', # formato de fecha
    handlers=[logging.StreamHandler()] # Indica donde se va a mostrar la información
)

# Función que va a crear los datos sintéticos
def create_data(locale: str) -> Faker:
    logging.info(f"Created synthetic data for {locale.split('_')[-1]} country code.") # Registra el país
    return Faker(locale)

# Función para generar un registro
def generate_record(fake: Faker) -> list:
    # Se generan los datos random
    person_name = fake.name()
    user_name = person_name.replace(" ","").lower() # Se quitan los espacios de los nombres y todo se hace minúsculas
    email = f"{user_name}@{fake.free_email_domain()}"
    personal_number = fake.ssn() # Número del Seguro Social
    birth_date = fake.date_of_birth()
    address = fake.address().replace("\n",", ")
    phone_number = fake.mac_address()
    mac_address = fake.mac_address()
    ip_address = fake.ipv4()
    clabe = fake.iban()
    accessed_at = fake.date_time_between("-1y")
    session_duration = random.randint(0,36_000)
    download_speed = random.randint(0,1_000)
    upload_speed = random.randint(0,800)
    consumed_traffic = random.randint(0,2_000_000)

    # Regresar dato como una lista
    return [
        person_name, user_name, email, personal_number, 
        birth_date, address, phone_number, mac_address, 
        ip_address, clabe, accessed_at, session_duration, 
        download_speed, upload_speed, consumed_traffic
    ]

# Guardar los datos en una csv
# file_path es donde va a guardar
# rows es cuántos registros hará
def write_to_csv(file_path: str, rows: int) -> None:
    fake = create_data("es_MX")

    # Definir headers
    headers = [
        "person_name", "user_name", "email", "personal_number", 
        "birth_date", "address", "phone_number", "mac_address", 
        "ip_address", "clabe", "accessed_at", "session_duration", 
        "download_speed", "upload_speed", "consumed_traffic"
    ]

    with open(file_path, mode="w",encoding="utf-8",newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for _ in range(rows):
            writer.writerow(generate_record(fake))

    # Message log
    logging.info(f"Written {rows} records to the CSV file")


# Crea un ID
def add_id(file_name) -> None:
    df = pl.read_csv(file_name)
    # Generar IDs
    uuid_list = [str(uuid.uuid4()) for _ in range(df.height)]
    # Agregar una nueva columna para los IDs
    df = df.with_columns(pl.Series("unique_id", uuid_list))
    df.write_csv(file_name)

    logging.info("Added UUID to the dataset.")

# Actualizar accessed_at
def update_datetime(file_name: str, run: str) -> None:
    if run == 'next':
        current_time = datetime.now.replace(microsecond=0)
        yesterday_time = str(current_time - timedelta(days=1))
        # Leer el csv
        df = pl.read_csv(file_name)
        df = df.with_columns(pl.lit(yesterday_time).alias("accedded_at"))
        # Guardar el archivo
        df.write_csv(file_name)

        logging.info("Updated accessed timestamp.")


if __name__ == "__main__":

    # Logging starting of the process.
    logging.info(f"Started batch processing for {date.today()}.")

    # Define the output file name with today's date.
    # output_file = f"/work_2/data_2/batch_{date.today()}.csv"
    output_file = f"/Users/alejandrabm/BigDataCrashCourse/batch_{date.today()}.csv"
    # Aplica cuando tengo el archivo en el directorio BD_DrivenPath\chapter_2\work_2 
    # y un nivel abajo esta data_2

    # Define number of records: first run - 10_372; next runs random number.
    if str(date.today()) == "2026-05-26":
        records = random.randint(100_372, 100_372)
        run_type = "first"
    else:
        records = random.randint(0, 1_101)
        run_type = "next"
        # Generate and write records to the CSV.
    write_to_csv(f"{output_file}", records)

    # Add UUID to dataset.
    add_id(output_file)

    # Update the timestamp.
    update_datetime(output_file, run_type)

    # Logging ending of the process.
    logging.info(f"Finished batch processing {date.today()}.")

