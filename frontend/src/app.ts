import {createApp} from 'vue'
import {Button, Cell, CellGroup, Icon, Menu, MenuItem, Avatar, Popup, OverLay} from "@nutui/nutui-taro";
import './app.scss'
import Taro from "@tarojs/taro";

const App = createApp({
  created() {
    // 如果不存在则注册新用户
    const r = Taro.cloud.callContainer({
      path: "/user/register",
      method: "POST",
      data: {}
    })
    console.log(r)

    r.catch((reason) => {
      Taro.showModal({
        title: '网络错误',
        content: '连接到服务器时发生错误, 请稍后再试或反馈给我们: ' + JSON.stringify(reason),
        showCancel: false
      })
    })
  },
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
