from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from datetime import datetime, timedelta
import requests
import json


# Latitude and Longitude of kathmandu university
LATITUDE="27.6193"
LONGITUDE="85.5385"

POSTGRES_CONN_ID = "weather_data_postgres"
API_CONN_ID = "open_meteo_api"



default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days=1),
}



with DAG(
    dag_id='weather_etl_pipeline',
    default_args=default_args,
    schedule='@hourly',
    catchup=False
) as dags:
    @task()
    def extract_weather_data():
        """  Extract weather data from Open Meteo API  """


        # Use HTTP Hook to make API call

        http_hook = HttpHook(http_conn_id=API_CONN_ID,method='GET')

        endpoint = f"/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"

        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from API. Status code: {response.status_code}")
        

    @task()
    def transform_weather_data(weather_data):
        """ Transform the weather data to match the database schema """

        # Extract relevant fields from the API response
        current_weather = weather_data['current_weather']
        transformed_data = {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode'],
        }
        return transformed_data
    

    @task()
    def load_weather_data(transformed_data):

        """ Load the transformed data into PostgreSQL database """

        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()


        # create table if not exists
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Insert the transformed data into the database

        cursor.execute("""
            INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
            VALUES (%s, %s, %s, %s, %s, %s)      
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))

        conn.commit()
        cursor.close()
    


    # Define the ETL pipeline
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)