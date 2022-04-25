<template>
  <!--  <nut-cell-group title="account">-->
  <nut-cell
    class="account-card"
    title="TEST CARD"
    desc="设置">
    <template v-slot:icon>
      <img
        class="site-icon"
        src="/assets/images/mooc.png"
      />
    </template>
  </nut-cell>
  <!--  </nut-cell-group>-->
</template>

<script>
import {Toast} from '@nutui/nutui-taro';

export default {
  name: "account-card",
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

  border-radius: 0;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.site-icon {
  width: 30px;
  height: 30px;
  margin-top: 2px;
  margin-left: 10px;
  margin-right: 20px;
}

</style>
