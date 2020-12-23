# Elasticsearch Project 
### Query restaurants using Django + Elasticsearch.
#### Enviroment:
* Ubuntu: 18.04 
* Python: 3.7
* Backend: Django Framework
* Database: Redis, Elasticsearch(7.1.0)


#### Install Elasticsearch 7 with Kibana using Docker Compose (Single Node)
* cd ./Elasticsearch

```
$ sudo docker-compose up --build -d
```

* Kibana url: http://127.0.0.1:5601

![home](https://img.onl/DH7D0u)
![page](https://img.onl/IchY2X)


#### Elasticsearch Restful API

* Create Index 
```
PUT restaurant
{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "restaurant_id": {
                "type": "long"
            },
            "restaurant": {
                "type": "text"
            },
            "ratings": {
                "type": "float"
            },
            "price": {
                "type": "long"
            },
            "types": {
                "type": "text"
            },
            "areas": {
                "type": "text"
            },
            "spots": {
                "type": "text"
            },
            "descriptions": {
                "type": "text"
            },
            "created_time": {
                "type": "date",
                "format" : "yyyy-MM-dd HH:mm:ss.SSSSSS"
            }   
        }
    }
}
```

* Delete Index
```
DELETE /restaurant
``` 

* Retrieve Mapping Definitions for An Index
```
GET /restaurant/_mapping 
```

* Query Object
```
GET /restaurant/_search/
{ "size":1000,
  "query": {
    "bool": {
      "must": [
          {"match_phrase":{"areas":"台北市"}}
        ]
    }      
  }
} 
```


#### API :
| Endpoints      | Method |
| --------- | -----:|
| /api/articles/   |  POST|
| /api/categories/     |      GET|
| /api/recommend/     |      GET|
| /api/update/area/     |      POST|
| /api/update/category/     |      POST|
| /api/update/restaurant/     |      POST|