<template>
  <nut-cell
    class="profile-account-card"
    :title=accountData.title
    desc="查看详情"
    @click="testClick">
    <template
      #icon>
      <img
        class="profile-site-icon"
        :src=accountData.from
      />
    </template>
  </nut-cell>
</template>

<script lang="ts">
import {Toast} from '@nutui/nutui-taro';
import {AccountData} from "../../types/AccountData";
import {defineComponent} from "vue";

export default defineComponent({
  props: {
    accountData: Object as () => AccountData
  },
  setup() {
    const testClick = (event) => {
      Toast.text('click');
    };
    return {
      testClick,
    };
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
