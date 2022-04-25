<template>
  <view class="profile">

    <!-- 显示用户头像 -->
    <span class="avatar">
      <nut-avatar
        size="large"
        :icon="avatar_url"/>
      {{ nickname }}
    </span>

    <account_card></account_card>
  </view>
</template>

<script>
import {ref} from 'vue'
import account_card from "../../components/card/account_card";

export default {
  components: {account_card},
  setup() {
    const msg = ref('Hello world')
    const nickname = ref('Test Username')
    const avatar_url = ref('https://img12.360buyimg.com/imagetools/jfs/t1/143702/31/16654/116794/5fc6f541Edebf8a57/4138097748889987.png')
    return {
      msg, nickname, avatar_url
    }
  }
}
</script>

<style>

.avatar {
  position: relative;
  left: 1em;
  top: 1em;
}

</style>
