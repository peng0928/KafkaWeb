# Kafka Web 可视化数据查询

#### 介绍

> 1. 实时监控和统计数据
> 2. 创建、管理和查看主题
> 3. 支持 topic 名称的搜索、topic 的搜索（默认支持 topic 数据的前 200 字符~后 200 字符）

#### 软件架构

> **vue3**
> **fastapi**

#### 数据库

> **MongoDb**

#### 安装教程

##### git 下载

```
git clone https://github.com/peng0928/KafkaWeb.git
```

##### 前端

```
cd kafka-pro-ui
npm i
npm run serve
```

##### 后端

```
cd kafka-api
pip install -r requirements.txt
python debug.py

```

#### 使用说明

##### 首页

![](/api/static/fd8f41072f3e5a89b0459cf0a79876fb.png)

##### 集群

![](/api/static/07cd6cc936f1553886c7190b938dfeb3.png)

##### Topic

![](/api/static/51103dcc820d5902ab6a9fee23e97062.png)

###### topic 数据

![](/api/static/ecbacd48ff695d7db601b2d893cb88b1.png)

![](/api/static/ed3d85aeb9085085b124ac39a7215a8d.png)
