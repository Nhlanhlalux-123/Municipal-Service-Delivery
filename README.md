# Municipal Service Delivery Data Pipeline

A beginner-to-intermediate Data Engineering project that collects, cleans, validates, stores, integrates, and analyzes municipal service-delivery data together with historical weather data.

The project demonstrates an end-to-end ETL pipeline using Python, PostgreSQL, Docker, Apache Airflow, SQL, Pandas, automated testing, and external API data.

---

## Project Overview

Municipal service-delivery data can contain duplicate records, missing information, inconsistent capitalization, and other quality problems.

This project builds a data pipeline that:

1. Extracts municipal service requests from a CSV file.
2. Cleans and validates the data.
3. Detects duplicate and invalid records.
4. Loads clean records into PostgreSQL.
5. Extracts historical weather data from an external API.
6. Transforms the weather data into a consistent format.
7. Loads historical weather data into PostgreSQL.
8. Joins service requests with weather data using municipality and date.
9. Produces SQL-based reports and analysis.
10. Uses Apache Airflow to orchestrate the complete workflow.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │ Service Requests CSV│
                    └──────────┬──────────┘
                               │
                               ▼
                         ┌───────────┐
                         │  Airflow  │
                         │    DAG    │
                         └─────┬─────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             Service Pipeline     Historical Weather API
                    │                     │
                    ▼                     ▼
                Extract                Extract
                    │                     │
                    ▼                     ▼
               Transform              Transform
                    │                     │
                    ▼                     ▼
                  Load                  Load
                    │                     │
                    └──────────┬──────────┘
                               ▼
                         ┌───────────┐
                         │PostgreSQL │
                         └─────┬─────┘
                               │
                               ▼
                     SQL JOIN + Analysis
                               │
                               ▼
                           Reports
```

---

## Technologies

| Technology     | Purpose                               |
| -------------- | ------------------------------------- |
| Python         | ETL and application logic             |
| Pandas         | Data analysis                         |
| SQL            | Data querying and analysis            |
| PostgreSQL     | Persistent database                   |
| Docker         | Containerization                      |
| Docker Compose | Local infrastructure                  |
| Apache Airflow | Pipeline orchestration and scheduling |
| Open-Meteo API | Historical weather data               |
| unittest       | Automated testing                     |
| Git            | Version control                       |

---

## Project Structure

```text
Municipal-Service-Delivery/
│
├── data/
│   └── service_requests.csv
│
├── src/
│   ├── __init__.py
│   │
│   ├── config.py
│   ├── database.py
│   │
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── pipeline.py
│   ├── report.py
│   │
│   ├── historical_weather_extract.py
│   ├── historical_weather_transform.py
│   ├── historical_weather_load.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── service_request.py
│   │   └── historical_weather.py
│   │
│   └── repositories/
│       ├── __init__.py
│       ├── service_repository.py
│       └── historical_weather_repository.py
│
├── tests/
│   ├── test_models.py
│   ├── test_pipeline.py
│   ├── test_transform.py
│   ├── test_weather_transform.py
│   └── test_historical_weather.py
│
├── airflow/
│   ├── dags/
│   │   └── municipal_pipeline.py
│   ├── Dockerfile
│   └── docker-compose.yaml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

---

# ETL Pipeline

## 1. Extract

The service pipeline reads raw records from:

```text
data/service_requests.csv
```

Example:

```text
id,date,municipality,service,area,status
1,2026-01-05,Johannesburg,Water,Soweto,Resolved
2,2026-01-06,Johannesburg,Electricity,Alexandra,Pending
```

The weather pipeline retrieves historical daily weather data from the Open-Meteo API.

---

## 2. Transform

The service data is cleaned by:

* Removing duplicate IDs
* Removing records with missing required fields
* Removing unnecessary whitespace
* Standardizing capitalization
* Converting dates into proper date objects
* Producing a data-quality report

Example:

```text
 johannesburg  → Johannesburg
 WATER         → Water
 resolved      → Resolved
```

Rejected records are tracked with reasons such as:

```text
Duplicate ID
Missing: municipality
Missing: area
```

---

## 3. Load

Clean service records are loaded into PostgreSQL:

```text
service_requests
```

Historical weather records are loaded into:

```text
historical_weather
```

The pipeline uses conflict handling so that records can be safely processed more than once.

---

# Database Design

## service_requests

```text
id
date
municipality
service
area
status
```

## historical_weather

```text
municipality
date
temperature_mean
precipitation
weather_code
```

The important relationship between the tables is:

```text
municipality + date
```

This allows service requests to be matched with weather observations from the same municipality and day.

---

# SQL Integration

The main integration query joins the two datasets:

```sql
SELECT
    s.id,
    s.date,
    s.municipality,
    s.service,
    s.area,
    s.status,
    h.temperature_mean,
    h.precipitation,
    h.weather_code
FROM service_requests s
JOIN historical_weather h
    ON s.municipality = h.municipality
   AND s.date = h.date
ORDER BY s.date, s.id;
```

This produces a combined dataset containing:

```text
Service request
      +
Matching historical weather
```

The project also performs aggregation such as:

* Total requests
* Requests by service
* Requests by municipality
* Requests by status
* Resolution rate
* Requests occurring on days with measurable rainfall

These analyses describe relationships in the dataset; they do not by themselves establish that weather caused service requests.

---

# Data Quality

The pipeline produces a data-quality report showing:

```text
Records extracted
Duplicate records
Records with missing fields
Records successfully cleaned
Rejected records and reasons
```

Example:

```text
DATA QUALITY REPORT
-------------------
Records extracted: 16
Duplicate records: 1
Missing fields:    2
Records loaded:    13
```

---

# Object-Oriented Design

The project also uses OOP concepts to model the data domain.

For example:

```python
ServiceRequest(
    id=1,
    date="2026-01-05",
    municipality="Johannesburg",
    service="Water",
    area="Soweto",
    status="Resolved"
)
```

and:

```python
HistoricalWeather(
    municipality="Johannesburg",
    date="2026-01-05",
    temperature_mean=23.5,
    precipitation=4.2,
    weather_code=61
)
```

The project uses:

* Classes
* Objects
* Dataclasses
* Encapsulation
* Separation of concerns
* Repository pattern
* Domain models

This allows the data-engineering project to reinforce software-engineering and OOP skills at the same time.

---

# Repository Layer

Database access is separated from the rest of the application.

```text
Application logic
       ↓
Repository
       ↓
PostgreSQL
```

For example:

```text
ServiceRequestRepository
HistoricalWeatherRepository
```

The repositories handle SQL operations while transformation and orchestration code remains separate.

---

# Airflow

Apache Airflow orchestrates the complete workflow.

The DAG contains two main branches:

```text
Service Data
    ↓
Extract
    ↓
Transform
    ↓
Load
```

and:

```text
Historical Weather
    ↓
Extract
    ↓
Transform
    ↓
Load
```

Both branches must complete before the reporting task runs.

```text
Service Load ─────────┐
                      ├──→ Report
Weather Load ─────────┘
```

The pipeline can be scheduled using the Airflow DAG rather than relying on manual execution.

---

# Docker

Docker Compose provides the local infrastructure.

The project uses containers for:

```text
Python ETL
PostgreSQL
Airflow
```

This makes the development environment reproducible.

---

# Running the Project Locally

## Requirements

You should have:

```text
Python 3
Docker
Docker Compose
```

---

## Install Python dependencies

From the project root:

```bash
pip install -r requirements.txt
```

---

## Configure environment variables

Create a `.env` file containing your PostgreSQL configuration.

Example:

```env
POSTGRES_DB=municipal_services
POSTGRES_USER=municipal_user
POSTGRES_PASSWORD=municipal_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Do not commit `.env` to Git.

---

# Run the ETL Pipeline

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run the pipeline:

```bash
python3 -m src.main
```

Run the report:

```bash
python3 -m src.report
```

---

# Open PostgreSql

Connect PostgreSql:

```bash
docker exec -it municipal-postgres psql \
  -U municipal_user \
  -d municipal_services
```

List tables:

```bash
\dt
```

Count rows in the clean data:

```bash
SELECT COUNT(*) FROM service_requests;
```

List 5 historical weather data:

```bash
SELECT * FROM historical_weather LIMIT 5;
```

Run Join:

```bash
SELECT
    s.id,
    s.date,
    s.municipality,
    s.service,
    s.status,
    h.temperature_mean,
    h.precipitation
FROM service_requests s
JOIN historical_weather h
    ON s.municipality = h.municipality
   AND s.date = h.date
ORDER BY s.date, s.id;
```

---

# Run the Tests

```bash
python3 -m unittest discover -s tests -v
```

The tests cover areas such as:

* Data cleaning
* Duplicate detection
* Missing data handling
* Data-quality reporting
* Domain models
* Weather transformation
* Pipeline behavior
* Historical weather transformation
* SQL integration behavior

---

# Run with Docker

Build the project:

```bash
docker compose build
```

Start the pipeline:

```bash
docker compose up
```

---

# Run Airflow

Go to the Airflow directory:

```bash
cd airflow
```

Start Airflow:

```bash
docker compose up -d
```

Open:

```text
http://localhost:8080
```

The DAG is:

```text
municipal_service_pipeline
```

Trigger it from the Airflow interface or allow its configured schedule to execute it.

---

# Example Workflow

A typical pipeline execution looks like:

```text
Starting data pipeline...

Records extracted
        ↓
Data cleaned
        ↓
Invalid records rejected
        ↓
Clean records loaded into PostgreSQL
        ↓
Historical weather extracted
        ↓
Historical weather transformed
        ↓
Historical weather loaded
        ↓
Service requests + weather JOIN
        ↓
Report generated
```

---

# Key Data Engineering Concepts Demonstrated

This project was designed to practice the following concepts:

```text
ETL
Data Cleaning
Data Validation
Data Quality
CSV Processing
REST/API Data Extraction
SQL
SQL JOINs
Aggregation
PostgreSQL
Python
Pandas
Docker
Docker Compose
Airflow
Scheduling
Testing
Data Modeling
Repository Pattern
Domain Models
```

---

# Future Improvements

Possible future extensions include:

* Add more municipalities
* Add more service categories
* Add additional external data sources
* Add historical weather for larger time periods
* Add dashboards and visualizations
* Add PostgreSQL indexes for larger datasets
* Add CI/CD
* Deploy the pipeline to the cloud
* Use object storage for raw datasets
* Introduce a data warehouse
* Add monitoring and alerting

---

# Learning Goals

This project was built as a practical introduction to Data Engineering.

The main goal is to understand the complete journey of data:

```text
Raw Data
   ↓
Extraction
   ↓
Cleaning
   ↓
Validation
   ↓
Transformation
   ↓
Storage
   ↓
Integration
   ↓
Analysis
   ↓
Reporting
```

The project can later be expanded into a larger Data Engineering portfolio project as new tools and concepts are learned.

---
# Verification code

```
WTC-6B9GW23X
```
