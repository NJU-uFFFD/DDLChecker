<template>
  <view class="cate">
    <text>我是历史页！</text>
  </view>

</template>

<script>
import {ref} from 'vue'

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
