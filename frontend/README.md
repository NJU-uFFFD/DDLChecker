# 前端 taro-Vue3-TypeScript

## 目录

```
- config 编译选项
  - dev.js
  - index.js 
  - prod.js
- src 
  - pages 页面
    - home 首页
    - history 历史
    - profile 我的
  - components 组件
    - card 卡片
  - assets 资源
    - images 图片
    - styles 自定义风格
  - app.ts 小程序入口
  - app.config.ts 小程序编译选项
  - app.scss
  - index.html
- package.json
- tsconfig.json
- babel.config.js
- README.md
```

## 开发记录

### -2022/4/24 Sakiyary

1. 初始化项目为`pages`, `components`, `assets`, 有`.vue`文件的地方就不用`.scss`(不然还要Vue干吗).
2. 引入`@nutui`, 感觉不是很会套.
3. 试了一下`nutui`的`cell`组件, ~~并不是那么好用, 感觉不如自己写~~, 海星.
4. 只写了空壳, 函数都没有.
