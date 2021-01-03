# Elasticsearch Project 
### Query restaurants using Django + Elasticsearch.
#### Enviroment:
* Ubuntu: 18.04 
* Python: 3.7
* Backend: Django REST Framework
* Database: Redis, Elasticsearch(7.1.0)


#### Install Elasticsearch 7 with Kibana using Docker Compose (Single Node)
* cd ./Elasticsearch

```
$ sudo docker-compose up --build -d
```

* Kibana url: http://127.0.0.1:5601

![home](https://img.onl/DH7D0u)
![page](https://img.onl/IchY2X)

#### API :
| Endpoints      | Method |
| --------- | -----:|
| /api/articles/   |  POST|
| /api/categories/     |      GET|
| /api/recommend/     |      GET|
| /api/update/area/     |      POST|
| /api/update/category/     |      POST|
| /api/update/restaurant/     |      POST|


#### Elasticsearch Restful API

* Create Index 
```
PUT restaurant
{
    "settings": {
        "number_of_shards": 5, # 一經設定後就不能更改
        "number_of_replicas": 1 # 設定目前索引的備份數量
    },
    "mappings": {
        "dynamic":"strict", #從嚴模式，如果發現新欄位拋出例外。
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

* Retrieve Settings for An Index
```
GET restaurant/_settings
```

* Update Number of Replicas
```
PUT restaurant/settings
{
    "number_of_replicas":2
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
GET /restaurant/_search/  # _search表示搜索操作
{ "from": 100, # 分頁
  "size": 1000,
  "source": "restaurant",
  "query": {
    "bool": {
      "must": {
          "term":{
            "areas":"台北市"
            }
        }
    }      
  }
} 
```

### Elasticsearch 重要概念
#### 名詞介紹
* 底層使用Luance的全文搜索機制
* 讀寫效能上優於MongoDB

|       名詞       |    說明     |
| :---------:     | :---------:   |
| Index    |  是Elasticsearch儲存資料的地方，可以快速高效率地對索引中的資料進行全文索引。 |
| Shards    |  將一個index分成許多部分，每個部分就是一個Shards，實際上就是一個以Lucence為基礎的索引。索引建立後便不得更改，如更改將導致先前的路由值變成非法，造成數據遺失。  |
| Replicas |  索引容錯備份，防止資料遺失或用來做負載平衡   |
| Recovery   |  當有節點加入或退出叢集或故障節點重新啟動時，Elasticsearch會根據機器的負載情況，對索引分片shards進行重新分配。 | 
| Transport   |  代表Elasticsearch內部節點與用戶端的對話模式，預設使用TCP，同時支援HTTP、Thrift、Servlet、Memcached的傳輸協定 |  
| Document    |  是類似關聯式資料庫的一行資料，在一個Type裡的每一個Document都有一個唯一的ID作為區分。Document不需要有固定的結構，不同文件可以具有不同的欄位集合； |  
| Field   |  類似關聯是資料庫的某一列，是Elasticsearch資料儲存的最小單位。 |  
 

#### RDMS v.s Elasticsearch

|      關聯式資料庫        |    Elasticsearch     |
| :---------:     | :---------:   |
| Database    |  Index |
| Table    |  Type  |
| Row |  Document   |
| Column |  Field   |
| Schema |  Mapping   |



#### Elasticsearch 優點：
1. 高可用：高可用表現在容錯機制上，Elasticsearch叢集會自動發現新的或失敗的節點，重組和重新平衡資料，確保資料是安全和可存取的。
2. 模式自由: 動態mappimg機制可以自動檢測資料的結構和類型建立索引，並使資料可搜索。
3. 全文索引
4. 分散式： Elasticsearch水平擴充相當靈活，當資料規模比較小的時候可以使用小規模的叢集。隨著資料增長，需要更大的容量和更高的效能，此時只需增加更多的節點，Elasticsearch的自動發現機制會識別新增的節點並重新平衡分配資料。

#### Elasticsearch 重要參數說明
|      參數        |    說明     |
| :---------:     | :---------:   |
| node.master: true    |  指定該節點是否為master節點，預設叢集中第一台機器為master，如果這台機器故障就會重新選舉master |
| node.data: true    |  指定該節點是否存儲索引資料。  |
| index.number_of_shards: 5 |  預設索引分片個數   |
| index.number_of_replica: 1 |  預設索引備份個數。  |
| path.data: /path/to/data |  設定索引資料的儲存路徑，預設是Elasticsearch根目錄下的data資料夾。   |
| path.logs: /path/to/logs    |  設定紀錄檔的儲存路徑，預設是Elasticsearch根目錄下的logs資料夾。  |
| network.host: 192.168.0.1 |  設定綁定的IP地址。   |
| transport.tcp.port:9300 |  設定節點間互動的TCP端口，預設是9300  |
| http.max_content_length:100mb |  設定內容的最大容量   |
| http.cors.enable: false    |  是否使用http協定對外提供服務，預設為true  |


#### 讀寫許可權
|      參數        |    說明     |
| :---------:     | :---------:   |
|block.read_only:true|目前索引只允許讀不允許更改或寫入操作|
|block.read:true|目前索引不允許讀取操作|
|block.wirte: true|目前索引不允許寫入操作|


#### 版本控制
* 使用Elasticsearch的API進行資料更新的過程：
    讀取來源文件，對原文件進行更新操作（文件每被修改一次，文件版本編號會自動增加一次，Elasticsearch使用_version欄位確保所有的更新都是有序進行），更新操作執行完成後，再重新索引整個文件。不論執行多少次更新，最後儲存在Elasticsearch中的是最後一次更新後的文件。
* 外部版本控制：要求外部文件版本比內部版本新時，才能更新成功。
```
PUT restaurant/_doc/3000?version=5&version_type=true
```

#### 路由機制
* 大多數情況下，Elasticsearch查詢數據，需要檢查所有shards分片以便能檢索到相關資訊。
* 透過雜湊演算法，將具有相同雜湊值的文件放置到同一個主分片中。
```
shard = hash(routing) % number_of_primary_shards
```
* routing值可以是一個任意字串，預設將文件的id值作為routing值，透過雜湊函數根據routing字串產生一個數字，然後除以主切片的數量獲得一個餘數，餘數的範圍永遠是0到number_of_primary_shards-1，這個數字就是特定文件所在的分片。這種演算法會保持所有資料在所有分片的平均分佈，而不會導致資料傾斜。

* 叢集搜索機制：
    1. 查詢請求首先被叢集中的節點接收
    2. 接收到這個請求的節點，將這個查詢廣播到這個索引的每個分片上。
    3. 每個分片執行玩搜索查詢並傳回結果。
    4. 結果在通道節點上合併、排序並傳回給使用者。
* 路由優點:
    + 減少系統資源。
* 路由缺點:
    + 可能導致數據傾斜。
* 舉例：
```
    PUT website/_doc/1?routing=user123
    {
        "title": "My first blog entry",
        "text:": "Just trying this out..."
    }
```
```
GET /website/_search?routing=user123
```

#### 對映機制：
* 動態映射: Elasticsearch寫入資料之前不需建表，他會根據欄位的列別自動識別。

* 靜態映射類型: 寫入資料之前對欄位的屬性進行手動設定。
* 欄位類型簡介: 
    1. text: 如果一個欄位要被全文檢索搜尋，例如產品描述、新聞內容，應該使用text類型，字串會被分詞器分成一個一個詞項。
    2. keyword: 適用於索引結構化的欄位，例如email地址、主機名稱、狀態碼和標籤，通常用於過濾、排序，聚合。類型為keyword的欄位只能透過精確值搜索到，區別於text類型。

#### Elasticsearch 常見查詢：

|      類型        |    說明     |
| :---------:     | :---------:   |
| term query |  查詢用來尋找指定欄位中包含指定單字的文件，term查詢不會被解析，只有查詢詞和文件中的詞精確比對到才會被搜索到。  | 
| terms query | 用來查詢文件中包含多個詞的文件 |
|match query | 會對查詢敘述進行斷詞，斷詞後查詢敘述中一個詞項被比對到，文件就會被搜索到。 |
|match_phrase query | 首先會把query內容斷詞，斷詞器可以自訂，同時文件還需要滿足以下兩個條件才會被搜索到：(1) 斷詞後所有詞項都要出現在該欄位中 (2) 欄位中的詞項順序要一致 | 
|match_phrase query  | 用於搜索多個欄位 |
|exists query|回傳欄位中不可為空值的文件|
|prefix query|用於查詢某個欄位中以指定字首開始的文件| 
|bool query|把任意個簡單查詢組合在一起，使用must, should, must_not, filter選項來表示查詢之間的邏輯。|

```
GET /_search
{
    "query":
        "multi_match":{
            "query": "java程式設計",
            "fields": ["title, "*_name"]
        }
}
```
```
GET /_search
{
    "query":
        "prefix":{
            "description": "win"
        }
}
```