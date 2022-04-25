<template>
  <view class="profile">

    <!-- 显示用户头像 -->
    <nut-cell
      class="profile-card"
      :title=nickname
      :sub-title="我是测试者">
      <template v-slot:icon>
        <nut-avatar
          class="avatar"
          size="large"
          :icon="avatar_url"/>
      </template>
    </nut-cell>
    <view v-for="item in [1,1,1,1,1,1]">
      <account_card/>
    </view>

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
.profile-card {
  margin-top: 20px;
  align-items: center;
  border-radius: 0;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.avatar {
  margin-right: 20px;
}

.profile {
  background: #f9f9f9;
}

</style>
