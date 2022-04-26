<template>
  <view class="profile">
    <profile_card
      :nickname=nickname
      :avatar_url=avatar_url>
    </profile_card>
    <nut-cell-group
      class="account-group"
      title="账号管理"/>
    <view v-for="item in account_list">
      <account_card :account_item="item"/>
    </view>
  </view>
</template>

<script lang="ts">
import {ref, reactive, toRefs} from 'vue'
import account_card from "../../components/card/account_card.vue";
import profile_card from "../../components/card/profile_card.vue";
import {Account_List} from "../../types/Account_List";

export default {
  name: 'profile',
  components: {
    profile_card,
    account_card
  },
  setup() {
    const nickname = ref('Test Username')
    const avatar_url = ref('../../assets/images/test_avatar.png')
    const accounts = reactive<{ account_list: Account_List[] }>({
      account_list:
        [{aid: 1, title: "MOOC", from: "/assets/images/mooc.png"},
          {aid: 2, title: "SPOC", from: "/assets/images/spoc.png"},
          {aid: 3, title: "教学立方", from: "/assets/images/jxlf.png"},
          {aid: 4, title: "MOOC", from: "/assets/images/mooc.png"},
          {aid: 5, title: "SPOC", from: "/assets/images/spoc.png"},
          {aid: 6, title: "教学立方", from: "/assets/images/jxlf.png"},
          {aid: 7, title: "MOOC", from: "/assets/images/mooc.png"},
          {aid: 8, title: "SPOC", from: "/assets/images/spoc.png"},
          {aid: 9, title: "教学立方", from: "/assets/images/jxlf.png"},
          {aid: 10, title: "MOOC", from: "/assets/images/mooc.png"},
          {aid: 11, title: "SPOC", from: "/assets/images/spoc.png"},
          {aid: 12, title: "教学立方", from: "/assets/images/jxlf.png"},
          {aid: 13, title: "MOOC", from: "/assets/images/mooc.png"},
          {aid: 14, title: "SPOC", from: "/assets/images/spoc.png"},
          {aid: 15, title: "教学立方", from: "/assets/images/jxlf.png"},]
    })
    return {
      nickname,
      avatar_url,
      ...toRefs(accounts)
    }
  }
}
</script>

<style>
.account-group {
  margin-top: -20px;
  margin-bottom: -10px;
}

.profile {
  background: #f9f9f9;
}

</style>
