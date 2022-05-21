# 前端 taro-Vue3-TypeScript

## 目录结构

```
├── dist                        编译结果目录
|
├── config                      项目编译配置目录
|   ├── index.js                默认配置
|   ├── dev.js                  开发环境配置
|   └── prod.js                 生产环境配置
|
├── src                         源码目录
|   ├── assets                  资源文件目录
|   |   ├── images              图片文件目录
|   |   └── styles              自定义风格目录
|   |
|   ├── components              组件文件目录
|   |   ├── card                卡片组件目录
|   |   └── menu                菜单组件目录
|   |
|   ├── pages                   页面文件目录
|   |   ├── home                home 页面目录
|   |   |   ├── index.vue       home 页面逻辑+样式 (下同)
|   |   |   └── index.config.ts home 页面配置 (下同)
|   |   ├── history             history 页面目录
|   |   └── profile             profile 页面目录
|   |
|   ├── types                   数据接口文件目录
|   |
|   ├── app.ts                  项目入口文件
|   ├── app.scss                项目总通用样式
|   ├── app.config.ts           项目入口配置
|   └── index.html              H5项目额外配置
|
├── project.config.json         微信小程序项目配置
├── project.tt.json             字节跳动小程序项目配置
|
├── babel.config.js             Babel 配置
├── tsconfig.json               TypeScript 配置
├── .eslintrc                   ESLint 配置
|
├── package.json
└── README.md                   
```

## `Vue3`风格要求

1. 始终以 `key` 配合 `v-for` (感觉没什么用啊,排序也不能排,目前不知道能做什么)
2. 对于绝大多数项目来说，在单文件组件和字符串模板中，组件名称应该始终是 `PascalCase` 的——但是在 `DOM` 模板中是 `kebab-case` 的。
3. `JS/JSX` 中的组件名应该始终是 `PascalCase` 的，尽管在较为简单的应用中，只使用 `app.component` 进行全局组件注册时，可以使用 `kebab-case` 字符串。
4. 在单文件组件、字符串模板和 `JSX` 中，没有内容的组件应该是自闭合的——但在 `DOM` 模板里永远不要这样做。
5. 组件名称应该倾向于完整的单词，而不是缩写。
6. 在声明 `prop` 的时候，其命名应该始终使用 `camelCase`，而在模板和 `JSX` 中应该始终使用 `kebab-case`。
7. 多个 `attribute` 的元素应该分多行撰写，每个 `attribute` 一行。
8. 指令缩写 (用 `:` 表示 `v-bind`:，`@` 表示 `v-on`: 和用 `#` 表示 `v-slot`) 应该要么始终使用，要么始终不使用。

## 开发记录

### 2022/4/24 @Sakiyary

1. 初始化项目为 `pages`, `components`, `assets`, 有`.vue`文件的地方就不用`.scss`(不然还要Vue干吗).
2. 引入 `@nutui` , 感觉不是很会套.
3. 试了一下 `nutui` 的 `cell` 组件, ~~并不是那么好用, 感觉不如自己写~~, 海星.
4. 只写了空壳, 函数都没有.
5. 自定义风格中替换了主色调.

### 2022/4/25 @Sakiyary

1. `home` 和 `profile` 两页都用组件化的格式初始化了一下.
2. 当 `<script>` 区域报错的时候, 记得改为 `<script lang="ts">`.
3. 接着套.

### 2022/4/27 @Sakiyary

1. 按照风格要求重构代码.
2. 做好了排序显示, 被响应式和回调函数和 `emit` 整惨了, 耗了好久好久来debug.
3. 时间戳转换为字符串真的好麻烦, 如果用格式化还会有`24:40`或者`上午12:20`这种sb情况, 不用格式化的话还要手动补齐两位, 真的烦.
4. 现在类型转换还是有TS的类型警告, 想不出如何避免这个警告 (运行不会报错). (22/4/28: 用屎山修了)

### 2022/5/21 @Sakiyary

0. @lyc8503 懒得写开发记录, 那就我来写捏.
1. 已经做好了DDL的增删查, 改还没想好逻辑. 爬虫和后端接口在稳步推进.
2. 已经放弃了组件化, 传值真的会谢, 被迫屎山, 不过也确实没有什么复用很多的东西, 那就写在一起吧.
3. 还差历史页的全部和个人页的交互和修改DDL的逻辑.
4. 优化了很多之前写的捏.
