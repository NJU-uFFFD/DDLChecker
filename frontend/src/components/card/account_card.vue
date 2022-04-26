<template>
  <nut-cell
    class="account-card"
    :title=account_item.title
    desc="查看详情"
    @click="testClick">
    <template v-slot:icon>
      <img
        class="site-icon"
        :src=account_item.from
      />
    </template>
  </nut-cell>
</template>

<script lang="ts">
import {Toast} from '@nutui/nutui-taro';
import {Account_List} from "../../types/Account_List";

export default {
  name: "account-card",
  props: {
    account_item: Object as () => Account_List
  },
  setup() {
    const testClick = (event) => {
      Toast.text('click');
    };
    return {
      testClick,
    };
  }
}
</script>

<style>
.account-card {
  align-items: center;
  margin-left: 10px;
  margin-top: 0;
  margin-bottom: 5px;
  height: 40px;
  width: 95%;
  border-radius: 0;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.site-icon {
  width: 30px;
  height: 30px;
  margin-top: 2px;
  margin-right: 16px;
}

</style>
