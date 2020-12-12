### 简介

---

项目实现爬虫程序，用于爬取指定博主基本信息、发布的图片信息以及相关博文信息，存储方式为Mysql存储和Elastic search存储。

---

### 运行

---

```
python版本为 3.6.8 
ElasticSearch版本为6.8.7
程序入口为 main.py文件，运行该文件即可启动爬虫
在redis通过rpush到bloggerSpiderTask参数即可启动博主爬虫
在redis通过rpush到imageSpiderTask参数即可启动图片爬虫
在redis通过rpush到blogSpiderTask参数即可启动博文爬虫

示例输入：
	rpush bloggerSpiderTask 0123456789  --> 爬取id为0123456789用户的基本信息
    # 注意：在输入imageSpiderTask时，列表内的三个元素之间不能有空格，否则任务失败
	rpush imageSpiderTask [0123456789,1,10]  --> 爬取id为0123456789用户的照片墙的前10页图片
	rpush blogSpiderTask 0123456789  --> 爬取id为0123456789的博文
项目依赖项在requirements.txt文件中
```

---

### 介绍

---

```
项目采取fake-useragent随机产生假ua。
代理IP存储Redis中。
Cookie放在Redis中。
```

---

### 数据库设计

---
#### Mysql Database

| 表名              | blogger_info |              | |
| ----------------- | ------------ | ------------ | ----------------- |
| 字段名            | 类型         | 说明         | 长度 |
| uid | varchar      | 博主唯一标识 | 12 |
| name  | varchar         | 博主昵称     | 128|
| fansCount | integer      | 博主粉丝     | / |
| attentionCount | integer      | 博主关注     | / |
| postCount  | integer      | 博主发文数   | / |
| introduction   | varchar         | 博主简介     |256 |
| storageTime | datetime | 存储时间 | |
| headPortrait | varchar | 头像 | 256 |

---
| 表名              | img_info |              | |
| ----------------- | ------------ | ------------ | ----------------- |
| 字段名            | 类型         | 说明         | 长度 |
| imgId | varchar         | 图片唯一标识 |256 |
| imgUrl | varchar         | 图片链接 |256 |
| blogId   | varchar | 博文唯一标识 | 20 |
| userId | varchar | 博主唯一标识 | 12 |
| storageTime | datetime | 存储时间 | |

---

| 表名              | blog_info |              | |
| ----------------- | ------------ | ------------ | ----------------- |
| 字段名            | 类型         | 说明         | 长度 |
| blogId  | varchar      | 博文唯一标识 | 20 |
| likeCount      | integer | 博文点赞数 | / |
| commentCount | integer | 博文评论数 | / |
| relayCount    | integer      | 博文转发数 | / |
| detail      | text  | 博文详情 | |
| releaseTime    | datetime         | 博文发表时间 | |
| storageTime | datetime | 存储时间 | |
| authority | integer | 是否有权限查看 | |


---

#### ES Database

```
PUT IP:9200/sina_blog_info
```
```
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 0
  },
  "mapping": {
    "_doc": {
      "properties": {
        "blogId": {
          "type": "keyword"
        },
        "commentCount": {
          "type": "long"
        },
        "likeCount": {
          "type": "long"
        },
        "relayCount": {
          "type": "long"
        },
        "detail": {
          "type": "text"
        },
        "releaseTime": {
          "type": "keyword"
        },
        "storageTime": {
          "type": "keyword"
        },
        "authority": {
          "type": "long"
        }
      }
    }
  }
}
```

```
PUT IP:9200/sina_blogger_info
```

```
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 0
  },
  "mapping": {
    "_doc": {
      "properties": {
        "uid": {
          "type": "keyword"
        },
        "name":{
          "type":"text"
        },
        "fansCount": {
          "type": "long"
        },
        "postCount": {
          "type": "long"
        },
        "attentionCount": {
          "type": "long"
        },
        "introduction": {
          "type": "text"
        },
        "headPortrait": {
          "type": "keyword"
        },
        "storageTime": {
          "type": "keyword"
        }
      }
    }
  }
}
```

```
PUT IP:9200/sina_img_info
```

```
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 0
  },
  "mapping": {
    "_doc": {
      "properties": {
        "imageId": {
          "type": "keyword"
        },
        "imageUrl": {
          "type": "keyword"
        },
        "userId": {
          "type": "keyword"
        },
        "blogId": {
          "type": "keyword"
        },
        "storageTime":{
          "type":"keyword"
        }
      }
    }
  }
}
```







