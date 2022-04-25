<template>
  <nut-cell-group title="account">
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
  </nut-cell-group>
</template>

<script>
import {Toast} from '@nutui/nutui-taro';

export default {
  name: "account_card",
  setup() {
    const testClick = (event) => {
      Toast.text('click');
    };
    return {

    };
  }
}
</script>

<style scoped>

</style>
