<template>
  <!--  <nut-cell-group title="DDL">-->
  <nut-cell
    class="ddl-card"
    :title=ddl_item.title
    :sub-title=ddl_item.ddl_time
    desc="查看详情"
    @click="testClick">
    <template v-slot:icon class="t-icon">
      <img
        class="site-icon"
        :src=ddl_item.from
      />
    </template>
  </nut-cell>
  <!--  </nut-cell-group>-->
</template>

<script lang="ts">
import {ref} from 'vue';
import {Toast} from '@nutui/nutui-taro';
import {DDL_List} from "../../types/DDL_List";

export default {
  name: "ddl_card",
  props: {
    ddl_item: Object as () => DDL_List
  },
  setup() {
    const switchChecked = ref(true);
    const testClick = (event) => {
      Toast.text('点击事件');
    };
    return {
      testClick,
      switchChecked,
    };
  }
}
</script>

<style>
.ddl-card {
  margin-top: 12px;
  margin-bottom: 10px;
  align-items: center;
  margin-left: 10px;
  width: 95%;
  height: 100px;
  border-radius: 50px;
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
