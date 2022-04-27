## 就当这是个开发记录了...

### 目录

```
 - app.py 程序入口
 - routes 后端 API
   -rules.py json输入ji'o
   - utils.py 常用函数
   - exts.py 防止循环引用
   - account.py 用户账号管理
   - ddl.py 用户ddl管理
   - form.md 前后端数据交流格式
 - db 数据层
 - crawler
   - auth.py 登录认证
   - fetch.py 爬虫获取数据
```

## Test Resources

### ddl_add:

```
{
	"title": "Leo",
	"content": "wssbwssbwssbwssbwssbwssbwssb",
	"ddl_time": -1658453270035,
	"tag": "1",
	"course_uuid": "84ab1-1-0c-3e09-406e-b13b-bc431903e02f"
}
```



#### 2022/4/18

对接微信 API ing...

#### 2022/4/14 @lyc8503

逐步开始写一些爬虫相关的模块, 如何调用还要看云函数的用法.
