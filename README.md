# DDLChecker - ���

队名: `���` (可读作 `\uFFFD` `锟斤拷`  `乱码` etc.) 

队员:  LeoDu (队长)  BobHuang  Lyc8503  Sakiyary

Github Organization: [NJU-EL2022-uFFFD](https://github.com/NJU-EL2022-uFFFD) (仓库已设置 `private`, 在比赛完赛前不会开源)

[![DeepSource](https://deepsource.io/gh/NJU-EL2022-uFFFD/DDLChecker.svg/?label=active+issues&show_trend=true&token=QHJQLzy3d-4UJKOWzWsn0m6h)](https://deepsource.io/gh/NJU-EL2022-uFFFD/DDLChecker/?ref=repository-badge)

## 体验版预览

![o_abl4u4jtIL22vpvwwLPlPdVvu4](assets/README/o_abl4u4jtIL22vpvwwLPlPdVvu4-16539222835792.jpg)

若想体验，请私聊小队成员~

## 目录

```

├─.github
│  └─workflows
├─backend
│  ├─src
│  │  ├─crawler
│  │  │  └─crawlers
│  │  ├─db
│  │  ├─routes
│  │  │  └─rules
│  │  ├─service
│  │  └─util
│  │      └─sensitive_words_blocking
│  └─test
└─frontend
    ├─config
    └─src
        ├─assets
        │  ├─images
        │  └─styles
        ├─components
        │  └─card
        ├─pages
        │  ├─accountadd
        │  ├─community
        │  ├─courseddl
        │  ├─history
        │  ├─home
        │  └─profile
        ├─types
        └─util
```

## 功能

### 首页

- 展示DDL
  - 筛选功能: 已完成/ 未完成; 已超时/未超时; tag: "无tag"/ "紧急"/ "宽松"
  - 筛选功能页: 全选/反选
  - 排序功能: 由近至远/ 由远至近
  - 查看详情：
    - tag
    - 剩余时间/是否超时
    - ddl内容
- 添加DDL
  - 标题
  - 日期选择
  - 详情
  - tag选择
- 完成DDL
  - 点击对勾
- 修改DDL
- 删除DDL: 左滑
- 提醒DDL: 左滑, 访问系统日程

### 统计

- DashBoard
  - 总完成率
  - 已完成
  - 剩余紧急
  - 已超时
- 日历
  - 显示与ddl有关的日期: 点击后可查看详细情况

### 社区

主界面显示所有的爬取的/ 用户自主添加的课程

- 订阅: 在主界面订阅课程之后, 该课程的所有爬取的ddl将被自动添加到用户ddl中
- 添加课程: 可以添加无法从平台上爬取的课程, 添加之后, 所有用户均可订阅
- 删除课程: 可以删除自己添加的课程, 当该课程内存在DDL时无法删除
- 课程内ddl界面:
  - 展示所有爬取的/用户在该课程内创建的ddl, ddl详情页内可以展示该DDL的来源(系统自动爬取/其他用户添加)
  - 添加ddl: 向该课程贡献ddl, 贡献ddl之后, 其他用户均可以添加该条ddl
  - 删除ddl: 用户可以删除自己向课程贡献的ddl, 删除该ddl之后, 其他用户已经添加到自己列表的ddl不会受到影响

### 我的

- 更改用户名和头像:
  - 提供30个头像选择
- 账号管理:
  - 目前提供中国大学MOOC/南大SPOC/教学立方三个账号可供添加, 往后开放api将支持更多平台
  - 删除账号: 左滑删除
- 设置
