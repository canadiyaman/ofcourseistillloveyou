
# You can find some helpers below

- First you need to start all services using docker command
    ```shell
    docker-compose up --build
    ```


- Generate Random 50K Data
    ```shell
    chmod +x generate_data.sh
    ./generate_data.sh
    ```


- Insert data manually
    ```shell
      curl --location 'http://127.0.0.1:8000/api/v1/vehicle-telemetry' \
      --header 'Content-Type: application/json' \
      --data '{
          "latitude": 32.32,
          "longitude": 32.32,
          "plate_number": "00 ABC 99",
          "timestamp": "12.12.2024 13:27:32"
      }'
    ```


- Get Data by Given Date Range

    ```shell
    curl --location 'http://127.0.0.1:8000/api/v1/vehicle-telemetry?start_date=2024-12-01&end_date=2024-12-30'
    ```


#### Access Celery flower Interface to see Celery tasks:
    http://localhost:5555/tasks

### Access Kibana Interface to see Elasticsearch data
    http://localhost:5601/
