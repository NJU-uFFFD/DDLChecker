import {createApp} from 'vue'
import store from './store'
import './app.scss'

const App = createApp({
  onShow(options) {
  },
})

App.use(store)

export default App
