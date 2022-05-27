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
import {request} from "../../util/request";

export default {
  name: 'profile',
  components: {
    ProfileCard,
    AccountCard
  },
  data() {
    return {
      account_list: []
    }
  },
  setup() {
    const nickname = ref('Test Username')
    const avatarUrl = ref('../../assets/images/test_avatar.png')


    function addAccount() {
      Taro.navigateTo({
        url: '/pages/accountadd/index'
      })
    }

    return {
      nickname,
      avatarUrl,
      addAccount
    }
  },
  beforeMount() {
    const r = request({
      path: "/account/list",
      method: "POST"
    })

    r.then((res) => {
      if (res.statusCode === 200 && res.data.code === 0) {
        this.account_list = res.data.data.account_list
      } else {
        throw JSON.stringify(res)
      }
    }).catch((reason) => {
      console.error(reason)
      Taro.showModal({
        title: '错误',
        content: '发生网络错误: ' + JSON.stringify(reason),
        showCancel: false
      })
    })
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
