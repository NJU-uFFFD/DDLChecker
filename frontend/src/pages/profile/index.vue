<template>
  <view class="profile">
    <ProfileCard
      :nickname=nickname
      :avatarUrl=avatarUrl>
    </ProfileCard>

    <nut-cell @click="addAccount"> + 添加账号</nut-cell>

    <nut-cell-group
      class="profile-account-group"
      title="账号管理"/>

    <view
      v-for="data in account_list"
      :key="data.account_id">
      <AccountCard :accountData="data"/>
    </view>
  </view>
</template>

<script lang="ts">
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
      account_list:
        [{account_id: 1, title: "MOOC", from: "/assets/images/mooc.png"},
          {account_id: 2, title: "SPOC", from: "/assets/images/spoc.png"},
          {account_id: 3, title: "教学立方", from: "/assets/images/jxlf.png"},
          {account_id: 4, title: "MOOC", from: "/assets/images/mooc.png"},
          {account_id: 5, title: "SPOC", from: "/assets/images/spoc.png"},
          {account_id: 6, title: "教学立方", from: "/assets/images/jxlf.png"},
          {account_id: 7, title: "MOOC", from: "/assets/images/mooc.png"},
          {account_id: 8, title: "SPOC", from: "/assets/images/spoc.png"},
          {account_id: 9, title: "教学立方", from: "/assets/images/jxlf.png"},
          {account_id: 10, title: "MOOC", from: "/assets/images/mooc.png"},
          {account_id: 11, title: "SPOC", from: "/assets/images/spoc.png"},
          {account_id: 12, title: "教学立方", from: "/assets/images/jxlf.png"},
          {account_id: 13, title: "MOOC", from: "/assets/images/mooc.png"},
          {account_id: 14, title: "SPOC", from: "/assets/images/spoc.png"},
          {account_id: 15, title: "教学立方", from: "/assets/images/jxlf.png"},]
    })

    function addAccount() {

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
.profile-account-group {
  margin-top: -20px;
  margin-bottom: -10px;
}

.profile {
  background: #f9f9f9;
}

</style>
