<template>
  <nut-cell
    class="profile-account-card"
    :title=getPlatformInfo(accountData.platform_uuid).name
    :desc=description
    @click="cardClick">
    <template
      #icon>
      <img
        class="profile-site-icon"
        :src=getPlatformInfo(accountData.platform_uuid).icon
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
  margin-bottom: 5px;
  height: 40px;
  width: 95%;
  border-radius: 0;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.profile-site-icon {
  width: 30px;
  height: 30px;
  margin-top: 2px;
  margin-right: 16px;
}

</style>
