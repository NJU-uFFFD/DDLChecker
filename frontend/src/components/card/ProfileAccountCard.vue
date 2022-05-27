<template>
  <nut-cell
    class="profile-account-card"
    :title="accountData!=null?getPlatformInfo(accountData.platform_uuid).name:'添加账号'"
    :desc=description
    @click="cardClick">
    <template #icon>
      <img
        class="profile-site-icon"
        :src="accountData!=null?getPlatformInfo(accountData.platform_uuid).icon:'/assets/images/add.png'"
      />
    </template>
  </nut-cell>
</template>

<script lang="ts">
import {Toast} from '@nutui/nutui-taro';
import {AccountData} from "../../types/AccountData";
import {defineComponent} from "vue";
import {getPlatformInfo} from "../../util/ui";


export default defineComponent({
  name: "ProfileAccountCard",
  props: {
    accountData: Object as () => AccountData,
    description: String
  },
  setup(props, {emit}) {
    const cardClick = () => {
      emit("onClick", props.accountData);
    }

    return {
      cardClick,
      getPlatformInfo
    }
  }
})
</script>

<style>
.profile-account-card {
  align-items: center;
  margin-left: 10px;
  margin-top: 0;
  margin-bottom: 8px;
  height: 50px;
  width: 95%;
  border-radius: 10px;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.profile-site-icon {
  width: 30px;
  height: 30px;
  margin-top: 2px;
  margin-right: 16px;
}

</style>
