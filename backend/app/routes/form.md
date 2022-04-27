# Data form

## 前端  -> 后端

- add_ddl:

  ```
  		"title" -> str (len 1 - 50)
  		"content" -> str (len 1 - 200)
  		"ddl_time" -> int
  		"tag" -> str
  		"course_uuid" -> uuid
  ```

- list_ddl:

  ```
  		"start" -> int(>=0)
  		"end" -> int(>=0)
  		"filter" -> dirt
  				"is_completed" -> int(0, 1)
  				"by_course" -> int(0, 1)
  				"by_tag" -> int(0, 1)
  ```

  



## 后端 -> 前端

- add_ddl:

  
