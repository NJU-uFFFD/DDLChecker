<template>
  <view class="index">
    <text>{{ msg }}</text>
  </view>
</template>

<script>
import {ref} from 'vue'
import './index.scss'
//
// export default {
//   setup () {
//     const msg = ref('Hello world')
//     return {
//       msg
//     }
//   }
// }

import Taro from '@tarojs/taro'
import {AtTabBar} from 'taro-ui'

export default class Index extends Taro.Component {
  constructor() {
    super();
    // super(...arguments)
    this.state = {
      current: 0
    }
  }

  handleClick(value) {
    this.setState({
      current: value
    })
  }

  render() {
    return (
      // <AtTabBar
      //   tabList={[
      //     {title: '待办事项', text: 8},
      //     {title: '拍照'},
      //     {title: '通讯录', dot: true}
      //   ]}
      //   onClick={this.handleClick.bind(this)}
      //   current={this.state.current}
      // />
      <AtTabBar
        fixed
        tabList={[
          {title: '待办事项', iconType: 'bullet-list', text: 'new'},
          {title: '拍照', iconType: 'camera'},
          {title: '文件夹', iconType: 'folder', text: '100', max: 99}
        ]}
        onClick={this.handleClick.bind(this)}
        current={this.state.current}
      />
    )
  }
}
</script>
