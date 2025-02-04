# Northwind Data Pipeline using Meltano, Airflow, and Postgres

### Project Description
This project demonstrates the creation of a data pipeline using the Northwind database provided by Microsoft for educational purposes. The pipeline integrates Meltano for ELT (Extract, Load, Transform), Apache Airflow for orchestration, and PostgreSQL for data storage. Notably, the order_detail table is not included in the original database and is instead provided as a CSV file.

### Features
* Data Extraction: Extract data from the Northwind database and the order_detail CSV file.
* Data Transformation: Use Meltano to transform the extracted data.
* Data Loading: Load the transformed data into a PostgreSQL database.
* Workflow Orchestration: Utilize Apache Airflow to orchestrate and schedule the data pipeline.

### Repository Structure
* init_and_config_meltano.ipynb: Jupyter Notebook with the commands for Meltano and Postgres configuration.
* docker-compose.yml: File used to create and configure the database on meltano
* airflow/: Contains Apache Airflow DAGs for orchestrating the pipeline.
* data/: Contains the order_detail CSV file, the sql to mount the database on postgres, also is used to upload and process the data.
* meltano/: Contains the meltano.yml file, used to configure the ELT process
* README.md: Project documentation.

## Getting Started

### Prerequisites
Python 3.8 or above
PostgreSQL
Apache Airflow
Meltano

### Installation
Clone the repository:

```
sh
git clone https://github.com/tigureis/northwind_data_pipeline_using_meltano_airflow_postgres.git
cd northwind_data_pipeline_using_meltano_airflow_postgres
```

Install dependencies:

 ```
sh
pip install -r requirements.txt
 ```

Set up PostgreSQL:

Create a PostgreSQL database.
Update the database connection details in the configuration files.

### Running the Pipeline

#### Start Apache Airflow:
 ```
sh
airflow standalone
 ```

Trigger the DAG:

* Access the Airflow web UI at http://localhost:8080.
* Trigger the DAG to start the data pipeline.

### Usage
* Explore the data using the Jupyter notebooks in the notebooks/ directory.
* Modify the DAGs in the dags/ directory to customize the pipeline.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.


### Acknowledgements
Northwind database
Meltano
Apache Airflow
PostgreSQL
