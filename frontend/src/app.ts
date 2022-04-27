import {createApp} from 'vue'
import {Button, Cell, CellGroup, Icon, Menu, MenuItem, Avatar, Popup, OverLay} from "@nutui/nutui-taro";
import './app.scss'
import Taro from "@tarojs/taro";

const App = createApp({
  onShow() {
  },
})

// 微信云托管初始化
Taro.cloud.init({
  env: "prod-8gf8jswafda304f9"
})

App.use(Button)
  .use(Cell)
  .use(CellGroup)
  .use(Icon)
  .use(Menu)
  .use(MenuItem)
  .use(Avatar)
  .use(Popup)
  .use(OverLay)

export default App
