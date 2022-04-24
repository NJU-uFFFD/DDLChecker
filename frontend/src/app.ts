import {createApp} from 'vue'
import {Cell, Icon, CellGroup} from "@nutui/nutui-taro";
import './app.scss'

const App = createApp({
  onShow() {
  },
})

App.use(Cell).use(CellGroup).use(Icon)

export default App
