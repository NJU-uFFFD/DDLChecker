import {createApp} from 'vue'
import {Button, Cell, CellGroup, Icon, Menu, MenuItem, Avatar} from "@nutui/nutui-taro";
import './app.scss'

const App = createApp({
  onShow() {
  },
})

App.use(Button).use(Cell).use(CellGroup).use(Icon).use(Menu).use(MenuItem).use(Avatar)

export default App
