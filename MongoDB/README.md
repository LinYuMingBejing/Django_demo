# Book Search Engine (Django + MongoDB)
#### Enviroment:
* Ubuntu: 18.04 
* Python: 3.7
* Backend: Django Framework
* Database: MongoDB
* Test: Swagger
* Monitoring Tool: Supervisor, Prometheus, Grafana
* Collecting Logs: Logstash, Kibana


#### Deploy Applications:
```
$ cd docker_prd
$ sudo docker-compose up --build -d
```

#### API :
| Endpoint      | Method |
| ---------     | -----  |
| /api/         |  GET   |
| /api/filter/  |  GET   |


* /api/filter/ QueryString

| Column Name      | Type | Descriptions |
| ----------- | -----| --------- |
|     title |  String|  Book Title |
|  publisher |      String| -|
|  author |      String| -|
|  subCategory |      String| Book Category|
|  price__lte |      Integer| Maximum Price|
|  price__gte |      Integer| Minimum Price|


#### Swagger
* http://localhost/swagger/
![swagger](https://img.onl/a4duwv)


#### Logstash + Kibana
* http://localhost:5601/app/kibana
![swagger](https://img.onl/iFVWZC)


#### Prometheus
* http://localhost:9090/targets
![prometheus](https://img.onl/uUzXnC)


#### Grafana
* http://127.0.0.1:3000
![grafana](https://img.onl/Y6LiK9)


>#### Django Prometheus Reference:
* https://www.sipios.com/blog-tech/monitoring