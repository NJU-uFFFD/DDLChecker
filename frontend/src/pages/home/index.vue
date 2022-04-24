<template>
  <view class="index">
    <ddl_card></ddl_card>
    <ddl_card></ddl_card>
    <ddl_card></ddl_card>
    <ddl_card></ddl_card>
    <ddl_card></ddl_card>
    <ddl_card></ddl_card>
  </view>
</template>

<script>
import {ref} from 'vue'
import ddl_card from "../../components/card/ddl_card";

export default {
  name: 'ddl_list',
  components: {
    ddl_card
  },
  setup() {
    const msg = ref('Hello world')
    return {
      msg
    }
  }
}
</script>

<style>
.index {
  background: #f5f5f5;
}
</style>
