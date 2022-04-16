<template>
  <view class="my">
    <text>我是个人页！</text>
  </view>
</template>

<script>
import {ref} from 'vue'
import './index.scss'

export default {
  setup() {
    const msg = ref('Hello world')
    return {
      msg
    }
  }
}
</script>
