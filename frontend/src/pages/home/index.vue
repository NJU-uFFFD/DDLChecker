<template>
  <view class="index">
    <view v-for="item in list">
      <ddl_card></ddl_card>
    </view>
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
    const list = ref([1, 2, 3, 4, 5, 6, 7, 8])
    return {
      msg,
      list
    }
  }
}
</script>

<style>
.index {
  background: #f5f5f5;
}
</style>
