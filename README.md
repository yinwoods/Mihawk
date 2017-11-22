🦅日志监控系统🦅


设计目的：为了能够监控用户日志中的异常并及时报警

---

### 监控类型：

* 日志格式(log_format)
* 日志内容(log_content)
* 日志产生速率(log_speed)

---
### 现有监控系统：

* 经典的ELK （只有监控，没有报警）
* Spark Streaming + ElasticSearch（只有监控，没有报警，适用于监控情况复杂，需要用spark streaming计算的情况；但能够做到实时监控，实效性较强）
* open-falcon （原生框架适用于对系统、服务的性能监控，对于数据本身的监控需要开发插件）

#### 本系统优点：

* 借助开源组件，开发迅速
* 接入open-falcon，能够以多种方式报警

#### 本系统缺点：


* 功能相对简单，难以支持复杂查询

日志监控报警系统设计如下：

![日志监控报警系统.png](http://on-img.com/chart_image/5a13dd13e4b0d53d979b9cec.png)

日志监控报警系统开发计划：

解析层、执行层以及监控层全部使用docker封装

解析层开发与监控层调研并行
大体开发完成后，再结合请求层、执行层迭代测试开发
