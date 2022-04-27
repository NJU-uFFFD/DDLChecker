# Data form

## 前端  -> 后端

- "ddl/add":

  ```
  		"title" -> str (len 1 - 50)
  		"content" -> str (len 1 - 200)
  		"ddl_time" -> int
  		"tag" -> str
  		"course_uuid" -> uuid
  ```

- "ddl/list":

  ```
  		"start" -> int(>=0)
  		"end" -> int(>=0)
  		"filter" -> dirt
  				"is_completed" -> int(0, 1)
  				"is_overtime" -> int(0, 1)
  				"by_course" -> int(0, 1)
  				"by_tag" -> int(0, 1)
  ```

- "ddl/delete":

  ```
  		"ddl_id" -> int(>=0)
  ```

  



## 后端 -> 前端

- "ddl/add":

  ```
  		"ddl_id" ->int(>=0)
  ```
  
- "ddl/list":

  ```
  		"ddl_list" -> list[{
                  "ddl_id" -> int(>=0)
                  "title" -> str (len 1 - 50)
                  "content" -> str (len 1 - 200)
                  "ddl_time" -> int
                  "tag" -> str
                  "course_uuid" -> uuid
              }
  		]
  ```

- "ddl/delete":

  ```
  		"ddl_id" ->int(>=0)
  ```

  
