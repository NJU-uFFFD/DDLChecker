<template>
  <view class="cate">
    <text>我是历史页！</text>
  </view>

  <button @click="test">点击我发起请求</button>
</template>

<script>
import {ref} from 'vue'
import Taro from "@tarojs/taro";

export default {
  name: "history",
  setup() {
    const msg = ref('Hello world')
    return {
      msg
    }
  }
}
</script>

<style scoped>

</style>
