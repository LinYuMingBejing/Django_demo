# Book Search Engine (Django + MongoDB)
#### Enviroment:
* Ubuntu: 18.04 
* Python: 3.7
* Backend: Django Framework
* Database: MongoDB
* Monitoring Tool: Supervisor, Prometheus, Grafana


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


* GET /api/filter/ QueryString
* QueryString

| Column Name      | Type | Descriptions |
| ----------- | -----| --------- |
|     title |  String|  Book Title |
|  publisher |      String| -|
|  author |      String| -|
|  subCategory |      String| Book Category|
|  price__lte |      Integer| Maximum Price|
|  price__gte |      Integer| Minimum Price|


#### Prometheus
* http://localhost:9090/targets
![prometheus](https://img.onl/uUzXnC)


#### Grafana
* http://127.0.0.1:3000
![grafana](https://img.onl/Y6LiK9)


>#### Django Prometheus Reference:
* https://www.sipios.com/blog-tech/monitoring