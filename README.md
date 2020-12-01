# Elasticsearch Project 
#### Query restaurants using Django + Elasticsearch.
#### Enviroment:
* Ubuntu: 18.04 
* Python: 3.7
* Backend: Django Framework
* Database: Redis, Elasticsearch


#### Install Elasticsearch 7 with Kibana using Docker Compose (Single Node)
* cd ./Elasticsearch

```
$ sudo docker-compose up --build -d
```

* Kibana url: http://127.0.0.1:5601

![comment](https://img.onl/DH7D0u)


#### API :
| Endpoints      | Method |
| --------- | -----:|
| /api/articles/   |  GET|
| /api/categories/     |      GET|
| /api/update/area/     |      POST|
| /api/update/category/     |      POST|
| /api/update/restaurant/     |      POST|