<template>
  <view class="cate">
    <text>我是历史页！</text>
  </view>

  <button @click="test">点击我发起请求</button>
</template>

<script>
import {ref} from 'vue'
import Taro from "@tarojs/taro";

async function test() {
  const r = await Taro.cloud.callContainer({
    path: "/test",
    method: "POST",
    data: {"test": 123}
  })

  console.log(r)
}


export default {
  name: "history",
  setup() {
    const msg = ref('Hello world')
    return {
      msg, test, test2
    }
  }
}
</script>

<style scoped>

</style>
