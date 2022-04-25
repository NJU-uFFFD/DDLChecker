import {createApp} from 'vue'
import {Button, Cell, CellGroup, Icon, Menu, MenuItem} from "@nutui/nutui-taro";
import './app.scss'

const App = createApp({
  onShow() {
  },
})

App.use(Button).use(Cell).use(CellGroup).use(Icon).use(Menu).use(MenuItem)

export default App
