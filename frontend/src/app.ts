import {createApp} from 'vue'
import {Button, Cell, CellGroup, Icon,} from "@nutui/nutui-taro";
import './app.scss'

const App = createApp({
  onShow() {
  },
})

App.use(Button).use(Cell).use(CellGroup).use(Icon)

export default App
