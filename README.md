## 简略实现了一个Django RESTFUL API后端

### 1. 用django简略写了博客后端和前端

### 2. 用docker compose将该网站部署

### 3. 增加Nginx反向代理，隐藏端口显示

## 效果图

[演示网站](http://117.72.175.93/)

<img width="1367" height="1009" alt="图片" src="https://github.com/user-attachments/assets/6c489488-695e-4c76-be83-f879ce997676" />

---

## 注意：节点分割线

`d23c0d4d6a30793f687aa0a551df7d88e57c4d4d`
该节点是前端有图形界面的最后一个节点，自此之后，访问URL返回JSON数据，暂时只优化后端API部分，初步目标满足RESTFUL API规范。

声明的链接代码仍保留最后一个节点的状态，并不会更新（20250725）。


## 初步实现并验证

实现了如下方法（django本地运行）：

| 请求链接 | 请求方法 |  用途 |
|--| --| -- |
| posts/ | GET | 展示已发布文章列表，倒序 |
| posts/ | POST | 创建新文章 |
| posts/id/ | GET | 访问文章详情 |
| posts/id/ | PUT | 更新现有文章 |
| posts/id/ | DELETE |  删除现有文章 |

用postman测试参数合法及不合法的情况，返回json数据及返回码均合乎预期。

## 效果图

<img width="1515" height="881" alt="图片" src="https://github.com/user-attachments/assets/25e8d241-c158-4ea4-ba0c-ffcab30289e4" />


## 继续完善前端

这时的后端是存在put、delete等方法，常规的html只能实现get、post请求，所以这里我们需要用js去实现。

前端部分我将其跟后端分离，放到另一个分支中，blog_frontend。