# ⛅ Weather ETL Pipeline using Apache Airflow & Docker

This project is an ETL (Extract, Transform, Load) pipeline built with Apache Airflow that fetches real-time weather data from the Open-Meteo API for Kathmandu University, transforms it, and loads it into a PostgreSQL database.

## 📌 Features

- Extracts current weather data from Open-Meteo API
- Transforms raw data into structured format
- Loads data into PostgreSQL
- Runs hourly using Airflow scheduler
- Dockerized for easy setup

## 🌍 Location

- **Latitude:** 27.6193
- **Longitude:** 85.5385
- **Location:** Kathmandu University, Nepal

## 🧰 Technologies Used

- Python
- Apache Airflow
- PostgreSQL
- Docker 
- Open-Meteo API

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/this-iskamal/Weather_Data_ETL_Pipeline.git
cd Weather_Data_ETL_Pipeline
```

### 2. Start Docker services

```bash
docker compose up
```

### 3. Access Airflow

Visit: http://localhost:8080

**Login:**
- Username: `airflow`
- Password: `airflow`

### 4. Access PG-Admin

Visit: http://localhost:5050

**Login:**
- Email: `admin@admin.com`
- Password: `admin`

## 🔗 Airflow Connections Setup

### HTTP API Connection

- **Conn ID:** `open_meteo_api`
- **Type:** HTTP
- **Host:** `https://api.open-meteo.com`

### PostgreSQL Connection

- **Conn ID:** `weather_data_postgres`
- **Type:** Postgres
- **Host:** `weather_data_etl_pipeline-postgres-1`
- **Login:** `airflow`
- **Password:** `airflow`
- **Database:** `postgres`
- **Port:** `5432`

### PG-Admin Server Configuration

- **Host name:** `server_name`
- **Type:** Postgres
- **Host name/address:** `weather_data_etl_pipeline-postgres-1`
- **Login:** `airflow`
- **Password:** `airflow`
- **Port:** `5432`
