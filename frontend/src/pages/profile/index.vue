<template>
  <view class="page">
    <scroll-view
      :scroll-y="true"
      style="height: 100vh;">
      <ProfileCard
        :nickname=nickname
        :avatarUrl=avatarUrl>
      </ProfileCard>


      <nut-cell-group
        title="账号管理"/>
      <AccountCard
        v-for="data in account_list"
        :key="data.id"
        :accountData="data"/>
      <AccountCard
        @click="addAccount"/>

      <nut-cell-group
        title="设置"/>
    </scroll-view>
  </view>
</template>

<script lang="ts">
import Taro from '@tarojs/taro';
import {ref, reactive, toRefs} from 'vue'
import AccountCard from "../../components/card/ProfileAccountCard.vue";
import ProfileCard from "../../components/card/ProfileProfileCard.vue";
import {AccountData} from "../../types/AccountData";

export default {
  name: 'profile',
  components: {
    ProfileCard,
    AccountCard
  },
  setup() {
    const nickname = ref('Test Username')
    const avatarUrl = ref('../../assets/images/test_avatar.png')
    const accounts = reactive<{ account_list: AccountData[] }>({
      account_list: []
      // [{id: 1, userid: 0, platform_uuid: "f15684f5-d870-4a9d-b859-e7eec3c6e3b5", fields: []}]
    })

    function addAccount() {
      Taro.navigateTo({
        url: '/pages/accountadd/index'
      })
    }

    return {
      nickname,
      avatarUrl,
      addAccount,
      ...toRefs(accounts)
    }
  }
}
</script>

<style>

.page {
  background: #f9f9f9;
}

.nut-cell-group__title {
  margin-top: 15px;
}

.nut-cell-group {
  height: 30px;
}

</style>
