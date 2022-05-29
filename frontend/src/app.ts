import {createApp} from 'vue'
import {
  Dialog,
  Button,
  Cell,
  CellGroup,
  Icon,
  Menu,
  MenuItem,
  Avatar,
  Popup,
  OverLay,
  Form,
  FormItem,
  TextArea,
  Input,
  DatePicker,
  Picker,
  Toast,
  CountDown,
  Swipe,
  Checkbox,
  CheckboxGroup,
  SearchBar,
  Divider,
  Grid,
  GridItem,
  CircleProgress,
  Calendar,
  Collapse,
  CollapseItem
} from "@nutui/nutui-taro"
import './app.scss'
import Taro from "@tarojs/taro"
import {request} from "./util/request"
import {ENV_ID, USE_CONTAINER} from "./config"


const App = createApp({
  created() {
    // 如果不存在则注册新用户
    const r = request({
      path: "/user/register",
      method: "POST",
      data: {}
    })
    console.log(r)

    r.then((res) => {
      console.log(res)
      try {
        if (res.data.data.new) {
          Taro.showModal({
            title: '新用户注册',
            content: 'TODO: 新手指引',
            showCancel: false
          })
        }
      } catch (e) {
        console.error(e)
      }
    }).catch((reason) => {
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
if (USE_CONTAINER) {
  Taro.cloud.init({
    env: ENV_ID
  })
}


App.use(Button)
  .use(Cell)
  .use(CellGroup)
  .use(Icon)
  .use(Menu)
  .use(MenuItem)
  .use(Avatar)
  .use(Popup)
  .use(OverLay)
  .use(FormItem)
  .use(Form)
  .use(TextArea)
  .use(Input)
  .use(DatePicker)
  .use(Picker)
  .use(Dialog)
  .use(Toast)
  .use(CountDown)
  .use(Swipe)
  .use(Checkbox)
  .use(CheckboxGroup)
  .use(SearchBar)
  .use(Divider)
  .use(Grid)
  .use(GridItem)
  .use(CircleProgress)
  .use(Calendar)
  .use(Collapse)
  .use(CollapseItem)

export default App
